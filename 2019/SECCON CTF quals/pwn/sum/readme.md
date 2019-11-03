# SECCON CTF - 2019

## pwn / 289 - sum

> sum.chal.seccon.jp 10001

### Solution

By [@kruztw](https://github.com/dreamisadream)

由於過了一段時間才回來寫 writeup, 記憶有些模糊, 這邊只簡單說明漏洞及利用方式, 詳細情形請見 exp.py.
程式的漏洞在於 read_ints 的 for 迴圈的判斷條件多了一個等號, 導致 total 的位址被覆蓋, 致使攻擊者能透過 total 任意寫入. 但 sum 函式會先將 total 清成 0 使得攻擊者無法透過部份寫入 got 位址, 好在 sum 是由 main 呼叫, 因此當 sum 返回值 > 5 而導致 main 呼叫 exit 時, stack 上仍保有剛剛輸入的值, 因此我們能將 exit got 寫入帶有 pop_rsp 的 gadget, 讓 rsp 跳到我們想要的位址 (bss), 最後, 只要該位址有我們事先構建好的 rop chain 就能控制程式的運行.