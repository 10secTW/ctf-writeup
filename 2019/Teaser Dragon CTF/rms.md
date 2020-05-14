# Teaser Dragon CTF - 2019

## web / 126 - rms

>
> I generally do not connect to web sites from my own machine, aside from a few sites I have some special relationship with. I usually fetch web pages from other sites by sending mail to a program that fetches them, much like wget, and then mails them back to me. ~ Richard Stallman
>
>Flag is at http://127.0.0.1:8000/flag
>
>IP: rms.hackable.software:1337
>

### Solution

By [@ScottChen]([https://author_profile](https://github.com/scott987))

The program send a request for you, but block the 127.0.0.1.
However if doesn't block 0.0.0.0
![IMGUR](https://i.imgur.com/QNM7zd5.png)

### Flag
```DrgnS{350aa97f27f497f7bc13}```