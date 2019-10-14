## EmojiiVM - 198 / Misc

It's time to test your emoji programming skill!

Make sure to check out readme.txt before you enter the challenge :)

`nc 3.115.122.69 30261`

Notice:

Make sure you send exact N bytes after you input N as your file size.

Otherwise the server might close the connection before it print out the flag !


Author: bruce30262

66 Teams solved.

[readme.txt](./readme.txt)


### Solution

by [@jaidTw](https://github.com/jaidTw)

Basically an assembly language challenge, solution must < 2000 bytes.
Computing branch target is bothering because address should be composed from 0 ~ 10, but we can use `NOP` padding to avoid affecting adderss.

[sol.em](./sol.em)
[misc.py](./misc.py)
