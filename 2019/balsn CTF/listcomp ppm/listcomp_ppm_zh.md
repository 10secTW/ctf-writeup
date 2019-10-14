# Balsn CTF 2019

## PPM / 371 - listcomp ppm

> Solve 3 super easy list-comp challenges!!!
>
> Short! Shorter!! Shortest!!!
> ```
> nc easiest.balsnctf.com 9487
> ```
> UPDATE: the challenge runs by python3.6
>
> UPDATE: the original code should already be list comprehension
>
> Author: hortune

### Solution

by [@jaidTw](https://github.com/jaidTw)
Credits to [@oToToT](https://github.com/oToToT), [@HexRabbit](https://blog.hexrabbit.io)

本題共分成三個演算法小題，每題的答案必須是單行的Python list comprehension，且有限制長度。如何將答案縮短到限制內是比較費時的部份。

這題的分工上，由隊友[@oToToT](https://github.com/oToToT)先寫一般解法，我再和[@HexRabbit](https://blog.hexrabbit.io)試著將答案轉換為List Comprehension。

題目和我們的答案如下：

#### Question 1

The first line would contain a positive integer N. Then there would be N lines below. Each line contains two integer A and B. Please output the corresponding A+B.


Example Input:
```
3
1 2
3 4
5 6
```

Example Output:
```
3
7
11
```
Input Length Limit: 75


本題相對單純，直接就能寫出list comprehension了
```python3
[print(sum(map(int, input().split()))) for i in range(int(input()))]
```

#### Question 2

This is the knapsack problem that you know. Sasdffan is going to buy some junk foods. However, he has only limited budgets M. Each junk food would have two attributes, the cost of buying the junk food and the value of eating the junk food. The first line contains two positive integers N and M. Then, there would be N lines below. Each line contains two positive integers v and c. (v: value, c: cost). Please output the maximum value that Sasdffan could get after consuming all the junk foods he bought. Caution: Each junk food could only be bought once.
1000 <= N <= 2000, 1 <= M <= 3000, 1 <= c <= 3000, v > 0


Example Input:
```
3 5
1 2
1 3
2 2
```
Example Output:
```
3
```

Input Length Limit: 200

本題原始的解法如下
```python3
n, m = map(int,input().split(' '))
dp = [0] * (m+1)
for i in range(n):
    v, c = map(int,input().split(' '))
    for j in range(m, c-1, -1):
        dp[j]=max(dp[j], dp[j-c]+v)
print(max(dp))
```

這題難度相對提昇不少，因為有幾個值必須保存，且還要進行list等操作，經嘗試後大致可以歸納出幾種轉換

* 設定新變數`A = B` 可以轉換為 `[... for A in [B]]`
* `A, B, ... = C, D, ...`可以轉換為 `[... for A, B, ... in [[C, D, ...]]]`
* 可以用[[expA, expB, ...] for ...]的形式來連續執行expression A, B, ...

比較困擾的是，沒辦法使用`=`賦值，若要改動`list`的元素則必須使用`list.insert()`搭配`list.pop()`來達成，考慮到長度，比較好的作法是用`dict`取代，以`dict.update()`進行更新

e.g. `A[i] = B` => `A.update({i: B})`

此外還有一些技巧有助於縮短長度：
* 盡量避免變數初始化時的相依來減少層數。以本題為例，`dp`的大小相依`m`，但題目已給了`M`的範圍，因此可以直接初始化成固定大小。
* 如果dict存取次數不多，改用dict.get()存取能指定key不存在時的預設值，以省略初始化的步驟。
* 若迭代器本身的值不重要，只要次數對就好，則可以改用`[... for _ in [0] * N]`來達到執行N次的效果。

最後答案如下：

```python3
[
    [
        [
            [
                [
                    D.update({j: max(D.get(j,0), D.get(j-c,0)+v)}) for j in range(M, c-1, -1)
                ] for v,c in [map(int, input().split())]
            ] for _ in [0] * N
        ], print(max(D.values()))
    ] for N, M, D in [
        [
            *map(int, input().split()),
            {}
        ]
    ]
]
```

去掉空白後為：

```python3
[[[[[D.update({j:max(D.get(j,0),D.get(j-c,0)+v)})for j in range(M,c-1,-1)]for v,c in[map(int,input().split())]]for _ in[0]*N],print(max(D.values()))]for N,M,D in[[*map(int,input().split()),{}]]]
```
長度：194

#### Question 3

Depth of the tree. There is a size N tree with node index from 0 to N-1. The first line is an integer N (tree size). Then, there would be N numbers in the next line each represents the father of the node. (0 is always the root). 10 <= N <=10000. Please notice that for any i, father[i] < i.


Example Input:
```
3
0 0 1
```

Example Output:
```
2
```

Input Length Limit: 300

原始解：
```python3
n = int(input())
f = list(map(int,input().split()))
q = []
d = [0]*n
g = [f.count(i) for i in range(n)]
for i in range(n):
    if g[i]==0:
        q+=[i]

for u in q:
    if u == 0:
        break
    d[f[u]]=max(d[f[u]],d[u]+1)
    g[f[u]] -= 1
    if g[f[u]]==0:
        q += [f[u]]
print(d[0])
```

List comprehension:
```python3
[
    [
        [
            [
                q.append(i) for i in range(n) if g[i] == 0
            ],
            [
                [
                    d.update({f[u]: max(d.get(f[u], 0), d.get(u, 0) + 1)}),
                    g.update({f[u]: g[f[u]] - 1}),
                    q.append(f[u] if g[f[u]] == 0 else 0)
                ] for u in q if u != 0
            ], print(d[0])
        ] for g in [{i: f.count(i) for i in range(n)}]
    ] for n, f, q, d in [
        [
            int(input()),
            [*map(int, input().split())],
            [],
            {}
        ]
    ]
]
```
去掉空白為：
```python3
[[[[q.append(i)for i in range(n)if g[i]==0],[[d.update({f[u]:max(d.get(f[u],0),d.get(u,0)+1)}),g.update({f[u]:g[f[u]]-1}),q.append(f[u] if g[f[u]]==0 else 0)]for u in q if u!=0],print(d[0])]for g in[{i:f.count(i) for i in range(n)}]]for n,f,q,d in[[int(input()),[*map(int,input().split())],[],{}]]]
```

長度：298

更新：比賽結束後我們才發現少看了`farther[i] < i`這個constraint，實際解法可以更短
