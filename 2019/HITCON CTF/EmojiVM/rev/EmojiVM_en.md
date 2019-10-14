# HITCON CTF Quals - 2019

## Reverse / 187 - EmojiVM

A simple VM that takes emojis as input! Try figure out the secret!


Author: bruce30262

77 Teams solved.

### Solution

By [@jaidTw](https://github.com/jaidTw)

Reverse the binary and will find it read the source file then load it into `std::wstring`. It picks a `wchar_t` from the code at once to interpret as an opcode.

Here's the type of all opcodes, we named it based on guessing its functionality.
* `NOP` 
* `ADD`, `SUB`, `MUL`, `MOD`, `XOR`, `AND`, `LT`, `EQ` : `op1 op op2`
* `JMP` : `ip = op`
* `JNZ`, `JZ` : `if(op1 cond 0) ip = op2`
* `PUSH`, `POP`
* `MVGPTRIO`, `WRGPTRIO` : read/write a byte to `GPTR[op1][op2]`
* `ALLOC`, `FREE` : allocate/release a type of space called "GPTR", at most 10 chunk, each size not exceeding 0x5DC.
* `RDSTRI`, `PRSTRI` : Read/Write `GPTR[op]`
* `DMPSTK` : Dump stack from top
* `PRINT` : Print stack top as number
* `EXIT`

This is a classical stack machine, operation will pop from the stack to get operands, and push it back after. All instructions are encoded as a single `wchar_t` except `PUSH`, which will additionally extract one more `wchar_t` behinds and push it onto the stack.

Then, we found there was a piece of code setting some kind of mapping during the initialization. After testing, we knew that it's the mapping of Emoji -> Opcode.
<img src="https://i.imgur.com/46vNN5n.png" width="1000"/>
There was another mapping below, which is for Emoji -> Number.
<img src="https://i.imgur.com/Q7p4xP3.png" width="1000"/>

After understanding how it works, we can build the [disassembler](../evd) and [assembler](../evas).
Then we disassemble `chal.evm` and mark the byte offset of each instruction to get [chal.d](./chal.d) for reading.

```
6808  PUSH 1;
6810  RDSTRI;
```

The `RDSTRI` at 6810 is reading our input. So we can split the code here. The part before is for initialization and printing messages, and the part after will check our flag. We keep decompile it manually to get [tmp2.d](tmp2.d)。

After printing the message, it allocates 2 arrays.
```
GPTR[2] = [24, 5, 29, 16, 66, 9, 74, 36, 0, 91, 8, 23, 64, 0, 114, 48, 9, 108, 86, 64, 9, 91, 5, 26, 0]
GPTR[4] = [142, 99, 205, 18, 75, 88, 21, 23, 81, 34, 217, 4, 81, 44, 25, 21, 134, 44, 209, 76, 132, 46, 32, 6, 0]
```
There are some kinds of transformation after reading the input.
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
the result will be compared to `GPTR[4]`, and if they are equal, input XOR `GPTR[2]` will be printed out, which is the flag.
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
Thus, we can get the input by doing the inverse of transformation at 7407 on `GPTR[4]`.
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
