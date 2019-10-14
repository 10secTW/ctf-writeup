from pwn import *
import string

r = remote('13.113.205.160','21700')

def read_menu():
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    return

def check(a):
    read_menu()
    r.sendline(b'1')    #select write
    r.recvline()
    r.sendline(a.encode().hex())    #send check
    read_menu()
    r.sendline(b'2')    #read hash
    return r.recvline()

read_menu()
r.sendline(b'1337') #copy flag
read_menu()
r.sendline(b'2')    #read flag hash
fhash = r.recvline()
print(fhash)

flag = 'hitcon{'
#flag = 'hitcon{xxd?XDD!ed45dc4df7d0b79}'

alph = string.printable[:-6]

while flag[-1] != '}':
    for a in alph:
        test = check(flag+a)
        print(test)
        if test == fhash:
            flag += a 
            print("="*40)
            print(flag)
            print("="*40)
            break
        print(flag+a)

r.interactive()
