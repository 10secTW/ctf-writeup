PUSH 10;  #GPTR 0 = " * "
ALLOC;
PUSH 10;  #GPTR 1 = " = "
ALLOC;
PUSH 10;  #GPTR 2 = "\n"
ALLOC;
PUSH 10;  #GPTR 3 = counters
ALLOC;

#################
PUSH 4;
PUSH 8;
MUL;

PUSH 0;
PUSH 0;
WRGPTRIO;

PUSH 0;
PUSH 10;
PUSH 4;
MUL;
PUSH 2;
ADD;

PUSH 1;
PUSH 0;
WRGPTRIO;
PUSH 0;

PUSH 4;
PUSH 8;
MUL;

PUSH 2;
PUSH 0;
WRGPTRIO;
###################
PUSH 4;
PUSH 8;
MUL;

PUSH 0;
PUSH 1;
WRGPTRIO;

PUSH 0;
PUSH 10;
PUSH 6;
MUL;
PUSH 1;
ADD;

PUSH 1;
PUSH 1;
WRGPTRIO;
PUSH 0;

PUSH 4;
PUSH 8;
MUL;

PUSH 2;
PUSH 1;
WRGPTRIO;
####################
PUSH 10;
PUSH 0;
PUSH 2;
WRGPTRIO;
PUSH 1;
PUSH 0;
PUSH 3;
WRGPTRIO; # init outer loop counter GPTR[3,0]=1
############ @l1 = 100
PUSH 1;
PUSH 1;
PUSH 3;
WRGPTRIO; # init inner loop counter GPTR[3,1]=1
############
PUSH 0;
PUSH 3;
MVGPTRIO;
PUSH 10;
EQ;
PUSH 10;
PUSH 10;
MUL;
PUSH 7;
PUSH 6;
MUL;
ADD; # exit if GPTR[3,0] == 1
JNZ; # jmp to @l1
PUSH 10;
PUSH 10;
MUL;
PUSH 7;
PUSH 6;
MUL;
ADD;
PUSH 1;
ADD;
JMP; # jmp to @l2
####################### @l1=142
        EXIT;
####################### @l2=143
        PUSH 1;
        PUSH 3;
        MVGPTRIO;
        PUSH 10;
        EQ;
        PUSH 2;
        PUSH 10;
        PUSH 10;
        MUL;
        PUSH 10;
        PUSH 8;
        MUL;
        ADD;
        SUB;
        JNZ;    # jmp to @l4
        PUSH 4;
        PUSH 10;
        PUSH 10;
        MUL;
        PUSH 2;
        MUL;
        SUB;
        JMP;    # jmp to @l5
####################### @l4=178 break
                PUSH 10;
                PUSH 10;
                MUL;
                PUSH 2;
                MUL;
                PUSH 10;
                PUSH 5;
                MUL;
                ADD;
                PUSH 7;
                ADD;
                JMP; # jmp to @l6
####################### @l5=196 print a line
        PUSH 0;
        PUSH 3;
        MVGPTRIO;
        PRINT;
        PUSH 0;
        PRSTRI;
        PUSH 1;
        PUSH 3;
        MVGPTRIO;
        PRINT;
        PUSH 1;
        PRSTRI;
        PUSH 0;
        PUSH 3;
        MVGPTRIO;
        PUSH 1;
        PUSH 3;
        MVGPTRIO;
        MUL;
        PRINT;
        PUSH 2;
        PRSTRI;
##################### inc inner counter
        PUSH 1;
        PUSH 3;
        MVGPTRIO;
        PUSH 1;
        ADD;
        PUSH 1;
        PUSH 3;
        WRGPTRIO;
##################### loop
        PUSH 10;
        PUSH 10;
        MUL;
        PUSH 7;
        PUSH 6;
        MUL;
        ADD;
        PUSH 1;
        ADD;
        JMP; # jmp to @l2 = 143
########## @l6=257
PUSH 0;
PUSH 3;
MVGPTRIO;
PUSH 1;
ADD;
PUSH 0;
PUSH 3;
WRGPTRIO; #GPTR[3,0] += 1
PUSH 10;
PUSH 10;
MUL;
JMP;
