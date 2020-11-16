# BalsnCTF - 2020

## Rev / 310 - babyrev

### Solution

By [@jaidTw](https://github.com/jaidTw)

壓縮檔中有幾個 Scala 的 JVM Class 檔案，我們先反編譯並稍微整理一下程式碼

```scala
object babyrev {
    def anon(a:Stream[Int], What:Seq[Seq[Int]]): Stream[Int] = {
        return a.sum #:: anon(a.flatMap(What), What)
    }

    def Main(args:Array[String]): Uint = {
        var What = Seq{Seq{0, 1, 2, 3}, Seq{0}, Seq{0}, Seq{0}}
        this.broken = anon(Stream({0}), What);
    }

    def Run() = {
        var a = ...
        var b = BigInt(broken.apply(60107) % Math.pow(2, 62)).toByteArray()
        var flag = ObjectRef.create("")
        0.to(a.length).forEach(i => {
            flag[i] = (char)(byte)(a[i] ^ b[i % b.length])
        })
            
        println("The flag is BALSN{" + flag + "}")
    }
}
```

從中可以看到`Main`裡有個內容固定的 byte array `a` 和另一個 byte array `b`，其值為`broken.apply(60107) % pow(2, 62)`。程式接著對`a`與`b`進行 bitwise-xor後就得到了`flag`。

`broken`裡面將一個`Seq`物件作為參數傳給了`flatMap`，看起來很奇怪，但總之跑看看就知道了。我在[Scastie](https://scastie.scala-lang.org/)上跑了以下程式碼

```scala
def anon(a:Stream[Int], What:Seq[Seq[Int]]): Stream[Int] = {
    return a.sum #:: anon(a.flatMap(What), What)
}

b.apply(1)
b.apply(2)
b.apply(3)
b.apply(4)
b.apply(5)
b.apply(6)
b.apply(7)
b.apply(8)
b.apply(9)
...
```

執行數次`b.apply()`得到的回傳值會是
```
6
6
24
42
114
240
582
1302
3048
6954
...
```

接著，試著不斷將數列中的每一項除以 3 並計算差值後可以發現某種規律

|Term|1|2|3|4|5|6|7|8|9|10|...|
|-|-|-|-|-|-|-|-|-|-|-|-|
||6|6|24|42|114|240|582|1302|3048|6954||
|$\div6$|1|1|4|7|19|40|97|217|508|1159|
|diff|||3|3|12|21|57|120|291|651|
|$\div3$|||1|1|4|7|19|40|97|217
|diff|||||3|3|12|21|57|120|
|$\div3$|||||1|1|4|7|19|40

透過觀察可以發現數列`S = <a_n> = {1, 1, 4, 7, 19, 40, ...}`，並且，這個數列的遞迴式為

* `a[n] = a[n-1] + 3 * a[n-2]`
* `a[1] = 1`
* `a[2] = 1`

同時我們的目標函數為`f(x) = 6 * a[x]`.

如此一來，用下方的 Python script 算出$f(60107)$之後就能解出flag了。

```python
S = [1]*70000

def f(x): return 6 * S[x]

for i in range(3, 60110):
    S[i] = S[i-1] + 3*S[i-2]

a = [71, 20, -82, 84, -45, -4, 25, -122, 77, 63, -107, 13, -111, -43, 43, -42, 96, 38, -88, 20, -67, -40, 79, -108, 77, 8, -75, 80, -45, -69, 25, -116, 117, 106, -36, 69, -67, -35, 79, -114, 113, 36, -112, 87, -67, -2, 19, -67, 80, 42, -111, 23, -116, -55, 40, -92, 77, 121, -51, 86, -46, -85, 93]
b = (f(60107) % 2**62).to_bytes(length=8, byteorder='big')

for i in range(len(a)):
    print(chr((a[i] ^ b[i % len(b)]) & 0xFF), end="")
```

```
BALSN{U_S01ved_this_W4rmUp_R3v_CH411eng!!!_W3lcom3_to_BalsnCTF_2020!!}
```
