# DefCamp CTF - 2019

## Pwn / 162 - secret

> Target: 206.81.24.129:1339
>
> Download binary
>
> Author: Andrei

### Solution

By [@kruztw](https://github.com/dreamisadream)

這題有兩個很明顯的 bug
1. printf(buf) => fsb
2. gets(buf) => bof

我們首先用 fsb leak 出 libc_base 和 canary 並計算 one_shot, 接著用 bof 將 one_shot 寫到 return address , return 後就 get shell 了.
