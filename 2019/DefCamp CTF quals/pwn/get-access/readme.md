# DefCamp CTF - 2019
###### Contributed by < `kruztw` >

## get-access - 101 / pwn

Can you pwn this?

Target: 206.81.24.129:1337
Author: Andrei


### Solution
題目沒給 binary 檔, 且 nc 過去後要我們輸入一些東西 , 通常這類型題目要麼不是簡單 buffer overflow, 不然就是 blind format string , 經過測試後發現是 blind format string
![01](https://github.com/10secTW/ctf-writeup/blob/master/2019/DefCamp%20CTF%20quals/pwn/get-access/get-access_01.png)

對於這種題目的解法, 第一步就是 leak 整個 binary file, 而在 leak 過程中就發現 flag 了.

![02](https://github.com/10secTW/ctf-writeup/blob/master/2019/DefCamp%20CTF%20quals/pwn/get-access/get-access_02.png)