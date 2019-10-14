# Google CTF - 2019

## Crypto / 92 - Quantum Key Distribution

> Description: Generate a key using Quantum Key Distribution (QKD) algorithm and decrypt the flag.
>
> https://cryptoqkd.web.ctfcompetition.com/qkd/
>

### Solution

By [@killua4564](https://github.com/killua4564)

- 從題目中發現測量出來的 bit 是由最後的 complex 做機率性的 random 產生，所以我們要確保能知道他每個 bit random 出來是 1 或 0
- 如果 base 是 x 的話就會被 rotate45 度，那又因為如果 qubits 都放差不多的值會被說不夠 random，所以就一樣 random base ，然後如果是 x 的話 rotate(-45) 度
- script 中選擇讓他永遠只產生出來 1，這樣我就不用管他 server random 的 base，題目又說 `announcement: Shared key (in hex), the encryption key is encoded within this key.` 如果是講 encode 就猜說應該是 xor 吧，於是得到這個 `946cff6c9d9efed002233a6a6c7b83b1`
- 再按照他題目給的 command 做
	- `$ echo "946cff6c9d9efed002233a6a6c7b83b1" > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key`
	- `$ echo "U2FsdGVkX19OI2T2J9zJbjMrmI0YSTS+zJ7fnxu1YcGftgkeyVMMwa+NNMG6fGgjROM/hUvvUxUGhctU8fqH4titwti7HbwNMxFxfIR+lR4=" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key`
	- `>>> CTF{you_performed_a_quantum_key_exchange_with_a_satellite}`
