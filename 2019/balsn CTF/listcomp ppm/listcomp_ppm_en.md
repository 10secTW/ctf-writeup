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

By [@jaidTw](https://github.com/jaidTw)
Credits to [@oToToT](https://github.com/oToToT), [@HexRabbit](https://blog.hexrabbit.io)

This challenge is composed of 3 algorithmic questions, answers to each should be a single lined Python list comprehension. Also, there are length limits for the answers, thus how to reduce the answer into the acceptable length would be the difficult part.


For this challenge, my teammate [@oToToT](https://github.com/oToToT) wrote the original solution first, Then, [@HexRabbit](https://blog.hexrabbit.io) and I tried to transform the answer into list comprehension.

The following are questions and our solutions:

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


This one is fairly simple, one familiar with list comprehension can easily write down:
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

This is our original solution:
```python3
n, m = map(int,input().split(' '))
dp = [0] * (m+1)
for i in range(n):
    v, c = map(int,input().split(' '))
    for j in range(m, c-1, -1):
        dp[j]=max(dp[j], dp[j-c]+v)
print(max(dp))
```

This one is much harder, because we need to do variable assignment and list operations. Several transformation rules were concluded.
* Setting a new variable`A = B` can be replaced by `[... for A in [B]]`
* `A, B, ... = C, D, ...`can be replaced by `[... for A, B, ... in [[C, D, ...]]]`
* Use [[expA, expB, ...] for ...] to execute expression `expA`, `expB`, ... sequentially.

However, `=` is not allowed. We have to use `list.insert()` followed by `list.pop()` to alter an element of `list`. Take the code length into consideration, it would be better to use a `dict` instead of a `list` because there's a method `dict.update()` which can update more than one elements at once.

e.g. `A[i] = B` => `A.update({i: B})`

Also, there's some tips to shorten the length,
* Avoid the dependencies while initializing variables to reduce the nesting level. Take this question as example, the size of `dp` depends on `m`, but the range of `M` is already known, so `dp` could be always initialized to a fixed size, thus `dp` and `m` could be initialized in the same expression.
* Try to use `dict.get()` to access `dict`, which can set the default value when the key is missing, to get rid of the initialization step of `dict`
* If the value of the iterator itself is useless, i.e. the iterator is only used for loop counting, replace `[... for i in range(N)]` by `[... for _ in [0]*N]`

After applying these reductions:
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

After stripping the whitespaces:
```python3
[[[[[D.update({j:max(D.get(j,0),D.get(j-c,0)+v)})for j in range(M,c-1,-1)]for v,c in[map(int,input().split())]]for _ in[0]*N],print(max(D.values()))]for N,M,D in[[*map(int,input().split()),{}]]]
```
Length：194

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

Original ver.：
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

List comprehension ver.:
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

Whitespaces stripped:
```python3
[[[[q.append(i)for i in range(n)if g[i]==0],[[d.update({f[u]:max(d.get(f[u],0),d.get(u,0)+1)}),g.update({f[u]:g[f[u]]-1}),q.append(f[u] if g[f[u]]==0 else 0)]for u in q if u!=0],print(d[0])]for g in[{i:f.count(i) for i in range(n)}]]for n,f,q,d in[[int(input()),[*map(int,input().split())],[],{}]]]
```
Length：298

Update : We found us missed the constraint `farther[i] < i` after the CTF ends, the solution could actually be much more shorter.
