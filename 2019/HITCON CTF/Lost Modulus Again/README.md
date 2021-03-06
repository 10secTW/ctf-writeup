# HITCON CTF Quals - 2019

## Crypto / 200 - Lost Modulus Again

>
> It seems something wrong with my modulus.
>
> [lma-96272ceb426c53449452d3618953eeb4daf07b74.tar.gz](./prob)
>
>
>
> Author: lyc
>
> 64 Teams solved.
>

### Solution

By [@oToToT](https://github.com/oToToT)


題目開起來發現他給你

![$e,\ e^{-1} \bmod{\varphi(pq)},\ q^{-1} \bmod{p},\ p^{-1} \bmod{q},\ \text{plain}^e\bmod{pq}$](https://latex.codecogs.com/svg.latex?e,\%20e^%7B-1%7D%20\bmod%7B\varphi%28pq%29%7D,\%20q^%7B-1%7D%20\bmod%7Bp%7D,\%20p^%7B-1%7D%20\bmod%7Bq%7D,\%20\text%7Bplain%7D^e\bmod%7Bpq%7D)

發現這是個經典的RSA加密演算法


根據中國剩餘定理我們可以知道

![$p(p^{-1}\bmod{q})+ q(q^{-1}\bmod{p})\equiv 1\bmod{pq}$](https://latex.codecogs.com/svg.latex?p%28p^%7B-1%7D\bmod%7Bq%7D%29+%20q%28q^%7B-1%7D\bmod%7Bp%7D%29\equiv%201\bmod%7Bpq%7D)

更進一步可以得到

![$p(p^{-1}\bmod{q})+ q(q^{-1}\bmod{p})=pq+1$](https://latex.codecogs.com/svg.latex?p%28p%5E%7B-1%7D%5Cbmod%7Bq%7D%29%2B%20q%28q%5E%7B-1%7D%5Cbmod%7Bp%7D%29%3Dpq%2B1)

所以

![$p(p^{-1}\bmod{q}-1)+ q(q^{-1}\bmod{p}-1)=pq+1-(p+q)=\varphi(pq)$](https://latex.codecogs.com/svg.latex?p%28p%5E%7B-1%7D%5Cbmod%7Bq%7D-1%29%2B%20q%28q%5E%7B-1%7D%5Cbmod%7Bp%7D-1%29%3Dpq%2B1-%28p%2Bq%29%3D%5Cvarphi%28pq%29)

同時也知道![$ed-1=k\cdot\varphi(pq), k\in\mathbb{Z}$](https://latex.codecogs.com/svg.latex?ed-1%3Dk%5Ccdot%5Cvarphi%28pq%29%2C%20k%5Cin%5Cmathbb%7BZ%7D)

而且![$ed-1$](https://latex.codecogs.com/svg.latex?ed-1)的bit數很接近![$pq$](https://latex.codecogs.com/svg.latex?pq)的bit數，所以我們可以直接枚舉![$k$](https://latex.codecogs.com/svg.latex?k)，然後在假定![$\varphi(pq)=\frac{ed-1}{k}$](https://latex.codecogs.com/svg.latex?%5Cvarphi%28pq%29%3D%5Cfrac%7Bed-1%7D%7Bk%7D)的情況下去嘗試解![$p$](https://latex.codecogs.com/svg.latex?p)跟![$q$](https://latex.codecogs.com/svg.latex?q)出來。


要解![$p$](https://latex.codecogs.com/svg.latex?p), ![$q$](https://latex.codecogs.com/svg.latex?q)的部分則是可以透過擴展歐基理德演算法解[貝祖等式](https://zh.wikipedia.org/wiki/貝祖等式)，求出所有可能的正整數![$p$](https://latex.codecogs.com/svg.latex?p),![$q$](https://latex.codecogs.com/svg.latex?q)出來，然後要注意一下在![$gcd(a, b)\neq 1$](https://latex.codecogs.com/svg.latex?gcd%28a%2C%20b%29%5Cneq%201)的情況下的擴展歐基理德演算法要好好處理一下


附個拿來算![$p$](https://latex.codecogs.com/svg.latex?p), ![$q$](https://latex.codecogs.com/svg.latex?q)的code
```python
from Crypto.Util.number import *
import math

e = 1048583
d = 20899585599499852848600179189763086698516108548228367107221738096450499101070075492197700491683249172909869748620431162381087017866603003080844372390109407618883775889949113518883655204495367156356586733638609604914325927159037673858380872827051492954190012228501796895529660404878822550757780926433386946425164501187561418082866346427628551763297010068329425460680225523270632454412376673863754258135691783420342075219153761633410012733450586771838248239221434791288928709490210661095249658730871114233033907339401132548352479119599592161475582267434069666373923164546185334225821332964035123667137917080001159691927
ipmq = 138356012157150927033117814862941924437637775040379746970778376921933744927520585574595823734209547857047013402623714044512594300691782086053475259157899010363944831564630625623351267412232071416191142966170634950729938561841853176635423819365023039470901382901261884795304947251115006930995163847675576699331
iqmp = 22886390627173202444468626406642274959028635116543626995297684671305848436910064602418012808595951325519844918478912090039470530649857775854959462500919029371215000179065185673136642143061689849338228110909931445119687113803523924040922470616407096745128917352037282612768345609735657018628096338779732460743

k_phi_N = e * d - 1

def exgcd(x, y):
    if y == 0:
        return (1, 0)
    else:
        b, a = exgcd(y, x%y)
        b -= (x//y)*a
        return (a, b)

a, b = exgcd(ipmq-1, iqmp-1)
g = math.gcd(ipmq-1, iqmp-1)

def getPQ(phi):
    phi_g = phi // g
    # a*(ipmq-1) + b*(iqmp-1) == g
    # (phi_g*a)*(ipmq-1) + (phi_g*b)*(iqmp-1) == phi
    aa, bb = a*phi_g, b*phi_g
    dlta = (iqmp-1)//g
    dltb = (ipmq-1)//g
    tmp_ = abs(aa) // dlta - 10

    aa += tmp_ * dlta
    bb -= tmp_ * dltb
    assert(aa*(ipmq-1)+bb*(iqmp-1) == phi)

    while aa < 0:
        aa += dlta
        bb -= dltb
    assert(aa*(ipmq-1)+bb*(iqmp-1) == phi)

    while bb > 0:
        assert(aa*(ipmq-1) + bb*(iqmp-1) == phi)
        if isPrime(aa) and isPrime(bb) and inverse(aa, bb) == ipmq:
            print('aa=%d\nbb=%d'%(aa,bb))
            assert(0)
        aa += dlta
        bb -= dltb

for i in range(2**18, 2**25):
    if k_phi_N % i == 0 and (k_phi_N // i) % g == 0:
        getPQ(k_phi_N // i)
```


