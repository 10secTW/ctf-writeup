# HITCON CTF 2019

## EmojiiVM - 198 / Misc

> It's time to test your emoji programming skill!
> Make sure to check out readme.txt before you enter the challenge :)
>
> `nc 3.115.122.69 30261`
>
> Notice:
> Make sure you send exact N bytes after you input N as your file size.
> Otherwise the server might close the connection before it print out the flag !
>
> Author: bruce30262
> 66 Teams solved.

題目指示：[readme.txt](./readme.txt)

### Solution

by [@jaidTw](https://github.com/jaidTw)

基本上就是練習寫組語，限制解答在2000 bytes內，比較麻煩的是branch target要用`0~10`慢慢拼，塞指令的時候會影響到後面target的位址，可以用`NOP`去做padding。

[sol.em](./sol.em)
[misc.py](./misc.py)
