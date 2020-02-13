# nullcon HackIM 2020

## re / 100 - returminator

### Solution

By [@jaidTw](https://github.com/jaidTw)

[`deploy.py`](./deploy.py)會根據list `o`從`blob`中讀取不同的片段，作為[`main`](./main)的輸入並執行。而這段輸入則會造成`main`被stack buffer overflow，之後`deploy.py`再根據`main`的return值和list `r`進行比對，只要全部都正確就會輸出`Yes!`

我寫了一段[script](./extract.py)從`blob`中把這些輸入的payload分割出來，並顯示反組譯後的內容，可以發現return值會根據`0x4040a0`起的buffer值而不同，而這段正是`flag`被`main`讀到記憶體後的位址，因此只要能使`deploy.py`的檢查通過就能找到flag。

總共有33份payload，根據內容和對應的`r`值可以建立出方程組
```
0: flag[0] + flag[2] + flag[4] - 0x64 = 208
1: flag[6] + flag[8] + flag[0xa] = 225
2: flag[0xc] + flag[0xe] + flag[0x10] = 237
3: flag[0x12] + flag[1] - flag[0x1e] = 20
4: flag[3] + flag[0x16] + flag[3] - 0x64 = 214
5: flag[5] + flag[0x1d] + flag[0x1c] - flag[7] - 0x64 = 183
6: flag[9] + flag[0x11] - flag[0xb]= 79
7: flag[0xd] + flag[0xf] + flag[0x14] - flag[0x13] - flag[0x1b] = 105
8: flag[0x15] + flag[0x17] + flag[0x17] = 207
9: flag[0x19] + flag[0x1a] = 217
10: flag[0x1e] = 125 ('}')
11: flag[9] = 66 ('B')
12: flag[8] = 123 ('{')
13: flag[0] = 104 ('h')
14: flag[1] = 97 ('a')
15: flag[2] = 99 ('c')
16: flag[3] = 107 ('k')
17: flag[4] = 105 ('i')
18: flag[5] = 109 ('m')
19: flag[6] = 50 ('2')
20: flag[7] = 48 ('0')
21: flag[0xb] + flag[0] = 202
22: flag[0x1d] = 111 ('o')
23: flag[0x1d] = 111 ('o')
24: flag[0x1d] - flag[0xd] = 29
25: flag[0x1c] - flag[0xe] = 63
26: flag[0x1c] + flag[0xf] = 223
27: flag[0] - flag[0x1b] = 36
28: flag[0x17]  - flag[0x18] = 0
29: flag[0x1a] + flag[0] - flag[1] = 124
30: flag[0x13] = 100
31: flag[0xb] + flag[0xc] = 219
32: flag[0x15] - flag[0x14] = 32 
```

最後可以解到剩下
```
2: dest[0xe] + dest[0x10] = 116
5: dest[0x1d] + dest[0x1c] = 222
7: dest[0xf] + dest[0x14] = 191
8: dest[0x15] + 2 * dest[0x17]= 207
25: dest[0x1c] - dest[0xe] = 63
26: dest[0x1c] + dest[0xf] = 223
28: dest[0x17] = dest[0x18]
32: dest[0x15] - dest[0x14] = 32
```
整理後
```
flag[0xe] = 144 - 2x
flag[0xf] = 16 + 2x
flag[0x10] = 2x - 28
flag[0x14] = 175 - 2x
flag[0x15] = 207 - 2x
flag[0x17] = flag[0x18] = x
flag[0x1c] = 207 - 2x
flag[0x1d] = 15 + 2x 
```
這部分再進行暴力解，當`x = 48`時得到`flag = hackim20{B4byR0pDo0dOod00duDoo}`
