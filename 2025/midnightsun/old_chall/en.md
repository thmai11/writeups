# Old Chall
## Crypto

## Given
- ssh connection to a server

## Solution

we have 
- flag.enc 
- .viminfo 
into the home folder

Get the vim encrypted file:,
Can't SCP so lets get the b64 to get that home:
```
VmltQ3J5cHR+MDEhiXDtq3IL60Xl0ay1vfDYxoixybLFlVe4xMzUaf+OPhRhhKQNEYXK8lgR7Ngw
2JUA1KCH6X3Zd07w7nnKrhnzfhW/I1a+I2VqobcRPjnwm7m9qcZ0sf1s5zsNCqJzE0XbM9MOPqZj
w3Y=
```

Its the good old known-text attack pkzip


The problem is, this is not a zip file. The header is in my way
```bash
dd if=flag.txt of=cipher.bin bs=1 skip=12
```

Because of the .viminfo on the server we know some plain text 
`The flag I'm planning `


Now, Using bkcrack:
```
bkcrack -o -12 -e -c cipher.bin -p plan.txt 
bkcrack 1.7.1 - 2024-12-21
[11:08:06] Z reduction using 14 bytes of known plaintext
100.0 % (14 / 14)
[11:08:06] Attack on 499070 Z values at index -5
Keys: 9fa69309 af4c72de 85998520
100.0 % (499070 / 499070)
[11:12:31] Keys
9fa69309 af4c72de 85998520
```

Having the keys:

```
bkcrack -c cipher.bin -k 9fa69309 af4c72de 85998520 -d flag_clear.txt
```

Content:
```
 planning to use in 2025 is:
midnight{w1nZ1p_m0r3_L1k3_v1mz1P_am1rit3}
Awesome flag, right?
```

`midnight{w1nZ1p_m0r3_L1k3_v1mz1P_am1rit3}`