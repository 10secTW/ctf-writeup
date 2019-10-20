# SECCON CTF Quals - 2019

## Misc / 110 - Beeeeeeeeeer

> Let's decode!
>
>    [Beeeeeeeeeer](./Beeeeeeeeeer)

### Solution

By [@jaidTw](https://github.com/jaidTw)
Credits to [@HexRabbit](https://blog.hexrabbit.io/), [@ScottChen](https://github.com/scott987)

拿到一段很亂的bash script，先把escaped character轉回來，簡單代換還原出[這份](./phase1.sh)，其中有一段：
```sh
export S1=$(echo aG9nZWZ1Z2EK |base64 -d);
```
會設定環境變數`$S1=hogefuga`，接著往下看到很長的一串base64。
```
echo -n VeryLongBase64..|base64 -d|gunzip|bash;
```

執行這段指令就能解出第二份[shell script](./phase2.sh)：
```sh
for k in $($(echo p2IkPt== |tr A-Za-z N-ZA-Mn-za-m|base64 -d) $((RANDOM % 10 +1)));
do l=$((RANDOM % 10 +1));
 for m in $($(echo ==gCxV2c |rev|base64 -d) $l);
 do echo -ne '\a';
 sleep 1;
 done;
 echo "How many beeps?";
 read n </dev/tty;
 export n;
 if [ "$n" -ne "$l" ];
then exit;
fi;
 done;
echo "echo -ne '\a';sleep 1;echo -ne '\a';sleep 1;echo -ne '\a';sleep 1;echo \"How many beeps?\";"| bash;
 read n </dev/tty;
 export n;
...
```
在這裡又設定了一個環境變數`$n`，不過前半段是混淆用的，因為下面會被覆蓋，根據
```sh
echo -ne '\a';
sleep 1;
echo -ne '\a'
sleep 1;
echo -ne '\a';
sleep 1;
echo "How many beeps?"
```
從此行能推斷`$n=3`，因此下一行`openssl` pass參數為`cccc`
```sh
echo VeryLongBase64...|base64 -d|openssl aes-256-cbc -d -pass pass:$(echo -n $n|md5sum |cut -c2,3,5,12) -md md5 2>/dev/null |bash;
```
最後再將此行執行得到第三份[shell script](./phase3.sh)。這次則是徹底的混淆了，不過整理後在末段可以看到：
```
... && printf "\n\033[?7l%1024s" " " && echo SECCON{$S1$n$_____};
```
已知`$S1`,`$n`，因此剩下只要解出`$_____`即可。
用分號斷行，逐行執行會發現前面在輸出字串，從第一次出現`$_____`的部份開始往後分析，將每個`${@:$((.*))}`的結構逐個`echo`就能還原出字元，可以發現後面接著就是
```sh
read _____ < /dev/tty
: password is bash;
```
代入flag後就得到`SEECCON{hogefuga3bash}`
