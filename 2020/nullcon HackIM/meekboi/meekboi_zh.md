# nullcon HackIM 2020

## pwn / 100 - meek boi

### Solution

By [@jaidTw](https://github.com/jaidTw)

題目可以輸入一段shellcode，會被fork後的child執行，但stdin, stdout, stderr全部被導到/dev/null，但沒有任何seccomp限制，只要開了socket連到我自己的機器上再開reverse shell即可。

[sol.py](./sol.py)
