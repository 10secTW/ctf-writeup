## Reverse - EmojiVM (187)

經由逆向binary，會發現題目讀取檔案以後，載入到`std::wstring`後開始直譯，每次取一個`wchar_t`解析OPCODE。
OPCODE共有以下幾種，我們根據猜測其功能進行命名：
* `NOP` 
* `ADD`, `SUB`, `MUL`, `MOD`, `XOR`, `AND`, `LT`, `EQ` : `op1 op op2`
* `JMP` : `ip = op`
* `JNZ`, `JZ` : `if(op1 cond 0) ip = op2`
* `PUSH`, `POP`
* `MVGPTRIO`, `WRGPTRIO` : 對`GPTR[op1][op2]`進行一個byte的讀寫
* `ALLOC`, `FREE` : 分配和釋放一種稱為GPTR的空間，最多可以分配10個，每個大小不超過0x5DC。
* `RDSTRI`, `PRSTRI` : Read/Write `GPTR[op]`
* `DMPSTK` : Dump stack from top
* `PRINT` : Print stack top as number
* `EXIT`

題目設計上是個典型的Stack Machine，運算時會從stack上pop取得運算元，運算完畢後再push回stack上，除了`PUSH`會額外往後讀取1個`wchar_t`並push到stack上以外，其餘指令都是單獨一個`wchar_t`。

接著，我們可以發現初始化時有一處似乎在設定某種mapping，測試後發現是emoji對應到運算子的mapping
![](https://i.imgur.com/46vNN5n.png)
下方還有另一段則是emoji到數字的mapping
![](https://i.imgur.com/Q7p4xP3.png)

得知運作方式後，就可以寫出[disassembler](../evd)和[assembler](../evas)了。

接著將`chal.evm`反組譯後，配合工具標上每條指令的byte offset得到[chal.d](./chal.d)開始閱讀。

```
6808  PUSH 1;
6810  RDSTRI;
```

以6810的`RDSTRI`作為分界，前面在輸出menu和初始化，後面則是檢查flag，接著開始根據分支指令切出basic block，然後手動反編譯得到[tmp2.d](tmp2.。

在輸出完歡迎訊息後配置了兩個陣列
```
GPTR[2] = [24, 5, 29, 16, 66, 9, 74, 36, 0, 91, 8, 23, 64, 0, 114, 48, 9, 108, 86, 64, 9, 91, 5, 26, 0]
GPTR[4] = [142, 99, 205, 18, 75, 88, 21, 23, 81, 34, 217, 4, 81, 44, 25, 21, 134, 44, 209, 76, 132, 46, 32, 6, 0]
```
讀取完input後中間有一段轉換
```
7407  i = 0;
      do {
7408    off = i % 4;
7425    if(off == 0)
          GPTR[3, i] = GPTR[1, i] + 30;
7474    else if(off == 1)
          GPTR[3, i] = 7 ^ (GPTR[1, i] - 8);
7527    else if(off == 2)
          GPTR[3, i] = ((GPTR[1, i] + 44) ^ 68) - 4;
7580    else if(off == 3)
          GPTR[3, i] = (GPTR[1, i] ^ 101) ^ (172 & 20)
7633    i += 1
7658  } while(i < 24)
```
得到的結果會和`GPTR[4]`進行比較，若相等則將輸入和`GPTR[2]` XOR並輸出
```
8075  i = 0
8084  off = 0
      do {
8093    if(GPTR[3, i] == GPTR[4, i]) {
8135      off += 1;
        } else {
8160      off -= 1;
        }
8179    i += 1;
8192  } while(i < 24)
8346  if(off != 24);
8385    GOTO @fail;
8407  i = 0;
      do {
8429    GPTR[2, i] = GPTR[1, i] ^ GPTR[2, i];
8437    i += 1;
8458  while(i < 24);
8534  GOTO @correct;
```
由此可知只要將`GPTR[4]`進行7407處的逆運算即可得到input。

```c
#include <stdio.h>
#include <stdlib.h>

int a[] = {24, 5, 29, 16, 66, 9, 74, 36, 0, 91, 8, 23, 64, 0, 114, 48, 9, 108, 86, 64, 9, 91, 5, 26, 0};
int b[] = {142, 99, 205, 18, 75, 88, 21, 23, 81, 34, 217, 4, 81, 44, 25, 21, 134, 44, 209, 76, 132, 46, 32, 6, 0};
int c[24];

int main(void) {
    for(int i = 0; i < 24; ++i) {
        if(i % 4 == 0) {
            c[i] = b[i] - 30;
        } else if(i % 4 == 1) {
            c[i] = (b[i] ^ 7) + 8;
        } else if(i % 4 == 2) {
            c[i] = ((b[i] + 4) ^ 68) - 44;
        } else if(i % 4 == 3) {
            c[i] = (b[i] ^ (172 & 20)) ^ 101;
        }
        putchar((c[i]) & 0xFF);
    }
}
```
```
$ gcc sol.c -o sol
$ ./sol
plis-g1v3-me33-th3e-f14g
$ ./sol | ./emojivm ./chalevm
*************************************
*                                   *
*             Welcome to            *
*        EmojiVM 😀😁🤣🤔🤨😮       *
*       The Reverse Challenge       *
*                                   *
*************************************

Please input the secret: 😍
hitcon{R3vers3_Da_3moj1}
```
