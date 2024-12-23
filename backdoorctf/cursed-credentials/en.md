# Cursed Credentials

We are given 
- cert9.db
- key4.db
- logins.json

I know this is a mozilla firefox password database as its not the first time i'm facing this in a CTF.

First we need to format the hash for hashcat (or john)

This was available on the internet: https://fossies.org/linux/hashcat/tools/mozilla2hashcat.py

```
$mozilla$*AES*3510a742f59b198e198922f0c9bc43cf8ab52bf3*dadd3df784b946b13619b7f09fdce2e7a34e3e0cd4069263a0517d683d003695*10000*040e6bb3481d3086ee025f5b4b5b0afb*9c55609a7548c032b1bee0a1d948cec5
```

Running hashcat on it and the good old classic rockyou.txt

```
$mozilla$*AES*3510a742f59b198e198922f0c9bc43cf8ab52bf3*dadd3df784b946b13619b7f09fdce2e7a34e3e0cd4069263a0517d683d003695*10000*040e6bb3481d3086ee025f5b4b5b0afb*9c55609a7548c032b1bee0a1d948cec5:phoenixthefirebird14

Password: phoenixthefirebird14
```

Using firefox-decrypt 

```
./firefox_decrypt.py 

Primary Password for profile 2ibaio8j.Default User: 

Website:   https://play.picoctf.org
Username: '4n0nym0u5'
Password: 'flag{n0_p@ssw0rd_15_s3cur3??}'
```

`flag{n0_p@ssw0rd_15_s3cur3??}`

And 44 Brutus, That roman-xor was h4rd!