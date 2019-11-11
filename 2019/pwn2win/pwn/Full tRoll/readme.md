# Pwn2Win CTF - 2019

## pwn / 223 - Full tROll

> We've found a HARPA system that seems impenetrable. Help us to pwn it to get its secrets!
> Server: 200.136.252.31 2222
> Server backup: 167.71.169.196 2222

### Solution

By [@kruztw](https://github.com/dreamisadream)

題目首先要求輸入 password 然後進行檢查, 如果檢查通過則印 secret.txt 的內容, 經過分析後得知正確的 password 為 VibEv7xCXyK8AjPPRjwtp9X , 輸入後果不其然拿到 secret , 但 secret 的內容是個毫無意義的網址, 內容包含 flag.jpg
如下圖所示
![flag.jpg](https://i.imgur.com/r8QJkRK.jpg)
利用 binwalk stegsolve 等工具分析, 都找不出什麼特別的地方, 而且這題的標籤也沒標示 misc, 題目還對 pwn it 設粗體, 這使我果斷放棄這張圖, 回去找程式的 bug, 果不其然, 在輸入 password 時存在 buffer overflow, 因為輸入中止條件為讀取失敗或吃到換行, 因此只要正常輸入就能造成 bof, 而 overflow 的字串可以蓋到讀取的檔名(正常是 secret.txt), 因此我就不斷的猜檔名, 像是 flag.txt flag 等, 但都不對, 無奈之下繼續看 code, 由於這題有開 canary 保護, 因此第一步一定是先 leak 出 canary, 而題目中唯一可以 leak 字串的地方只有 
`printf("Unable to open %.*s file!\n",0x30,param_2);`
只要將字串填到與 canary 相鄰, 再觸發該行, 就能 leak 出 canary, 接著就是要 leak 出 libc_base , 這位址可透過讀取 /prof/self/ 下的檔案得知, 由於只能讀一行, 所以讀取 /prof/self/maps 只能拿到 pie_base, 但除了 /prof/self/maps 外, /proc/self/syscall 也能 leak libc_base, /proc/self/syscall 會紀錄程式目前調用的 system call, 由於我們是呼叫 read 去讀檔, 自然 /proc/self/syscall 會紀錄 read 在 libc 的位址, 有了 libc_base 後, 我們只要在 return address 寫入 one_gadget 就能成功 get shell .

註:<br>
雖然這不是 flag 說的預期解, 但也值得參考看看
<br>
CTF-BR{Fiiine...Im_not_ashamed_to_say_that_the_expected_solution_was_reading_/dev/fd/../maps_How_did_y0u_s0lve_1t?}
