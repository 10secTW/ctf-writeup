# SECCON CTF Quals - 2019

## Misc / 110 - Beeeeeeeeeer

> Let's decode!
>
>    [Beeeeeeeeeer](./Beeeeeeeeeer)

### Solution

By [@jaidTw](https://github.com/jaidTw)

Credits to [@HexRabbit](https://blog.hexrabbit.io/), [@ScottChen](https://github.com/scott987)

Given a obfuscated bash script，convert escaped characters back first，then we get [this](./phase1.sh), which contains following:
```sh
export S1=$(echo aG9nZWZ1Z2EK |base64 -d);
```
This will export environment variable `$S1=hogefuga`.

Keep going and there was a very long base64 string.
```
echo -n VeryLongBase64..|base64 -d|gunzip|bash;
```
Execute this line then we get the second [shell script](./phase2.sh)：

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
Another environment variable `$n` will be set here. But the upper half is meaningless, because `$n` will be replaced in the following lines.
```sh
echo -ne '\a';
sleep 1;
echo -ne '\a'
sleep 1;
echo -ne '\a';
sleep 1;
echo "How many beeps?"
read n </dev/tty;
```
We inferred `$n=3`, since each `'\a'` is a beep. Then we got the pass of the `openssl` in next line was `cccc`
```sh
echo VeryLongBase64...|base64 -d|openssl aes-256-cbc -d -pass pass:$(echo -n $n|md5sum |cut -c2,3,5,12) -md md5 2>/dev/null |bash;
```
Finally, execute this to get the third [shell script](./phase3.sh).

There was something at the end.
```
... && printf "\n\033[?7l%1024s" " " && echo SECCON{$S1$n$_____};
```
`$S1`,`$n` were known, so we have to solve `$_____`.

We used semicolons to split the script into lines, and executed it line by line, then found first few lines were for printing strings. So we only analyzed the part after the first occurence of `$_____`.

By echoing each `${@:$((.*))}` structure, we recovered the characters they're representing, and soon we found the code following was
```sh
read _____ < /dev/tty
: password is bash;
```
So, substitue the `$_____` and get `SEECCON{hogefuga3bash}`
