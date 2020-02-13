# nullcon HackIM 2020

## re / 100 - returnminator

### Solution

By [@jaidTw](https://github.com/jaidTw)

[`deploy.py`](./deploy.py) reads different parts from `blob` depends on the list `o` as the input to `[main](./main)`. 
These input will overflow main's stack buffer, then `deploy.py` compares their return value to list `r`. We ggt a "Yes!" if every check are passed.

I wrote a [script](./extract.py) to extract these payload from `blob` and show their disassembly. I found return value varies based onthe content of buffer starting from `0x4040a0`, which is the location of the flag. Thus, if we pass the check in `deploy.py`, then we get the flag.

There are 33 payloads in total, thus we can build an equation system based on their contents and corresponding value in `r`.
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

After some easy substitution, I got
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
Then, bruteforce this part.
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
Got `flag = hackim20{B4byR0pDo0dOod00duDoo}` when `x = 48`
