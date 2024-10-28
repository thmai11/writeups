# memory-puzzle

# Description

```
The Consortium has concealed a critical file within a memory dump, protected by layers of digital obfuscation. Led by Simon Letti, participants must sift through the volatile memory landscape to locate a plaintext key that unlocks the encrypted file. Time is of the essence, as Roko's Basilisk threatens to distort the data with each passing moment. Can you unravel the puzzle before the Basilisk intervenes?

"Basilisk's whisper will not wait" echos through your mind as you enter the file.

(Note: If you choose to use volatility2.6, use profile Win10x64_19041)
```
File `memory-puzzle.rar`

## Develop by Trent (https://github.com/tkg1121)

From the get go the challenge does a shoutout to volatility. Never used it neither I have ever solved a windows challenge!

⚠️ I will use Volatility 3 during this writeup

In the archive
```
unrar l memory-puzzle.rar 

UNRAR 7.01 freeware      Copyright (c) 1993-2024 Alexander Roshal

Archive: memory-puzzle.rar
Details: RAR 5

 Attributes      Size     Date    Time   Name
----------- ---------  ---------- -----  ----
    ..A.... 6869221376  2024-10-18 02:45  memory-puzzle.raw
    ..A....        64  2024-10-04 22:53  flag.enc
----------- ---------  ---------- -----  ----
           6869221440                    2
```

```
$ file flag.enc memory-puzzle.raw
flag.enc:          data
memory-puzzle.raw: Windows Event Trace Log
```

So i will dump with volatility these 3 things:
(Also found an handy cheatsheet https://blog.onfvp.com/post/volatility-cheatsheet/ )
- `windows.pstree`
- `windows.filescan`

I found this line to be interesting
```
*** 1980        4976    notepad.exe     0xb1084122e080  5       -       1       False   2024-10-18 06:43:38.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\notepad.exe    "C:\Windows\system32\NOTEPAD.EXE" C:\Users\johndoe\Desktop\system_update.py     C:\Windows\system32\NOTEPAD.EXE
```
User `johndoe` was editing this file `C:\Users\johndoe\Desktop\system_update.py` with  `C:\Windows\system32\NOTEPAD.EXE` and we have the PID and PPID!
With the `windows.filescan`

```bash
cat file_scan_output | grep johndoe
[...]
# There was a lots of file but here the interesting one
0xb1083fcf40c0  \Users\johndoe\Desktop\system_update.py
0xb1084089e960  \Users\johndoe\Desktop\system_update.exe
[...]
```
Lets try a `windows.dumpfiles` on these 2 files shall we!

```bash
vol -f memory_puzzle.raw -o files/ windows.dumpfiles --virtaddr 0xb1083fcf40c0 # system_update.py virt adddress
vol -f memory_puzzle.raw -o files/ windows.dumpfiles --virtaddr 0xb1084089e960 # system_update.exe virt adddress
```

- system_update.py: volatility yield nothing
- system_update.exe: I get the file!

What is it?
```bash
file file.0xb1084089e960.0xb1083edb4550.DataSectionObject.system_update.exe.dat
file.0xb1084089e960.0xb1083edb4550.DataSectionObject.system_update.exe.dat: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c094c53ae90b55cff2d739824790963e767852f0, for GNU/Linux 3.2.0, not stripped
```

Strings?
```bash
# Here the interesting one
EVP_EncryptUpdate
EVP_aes_128_cbc
EVP_EncryptInit_ex
EVP_CIPHER_CTX_new
EVP_CIPHER_CTX_free
EVP_EncryptFinal_ex
[...]
SuperSecH
retKey12H
[...]
EVP_EncryptUpdate@OPENSSL_3.0.0
[...]
```

Ok ! I get that are the key part,
- SuperSecH
- retKey12H

Encryption is `aes-128-cbc`, and i might decrypt it with `OPENSSL_3.0.0`
So `SuperSecretKey12` is the key 

Lets do it!
```bash
openssl enc -d -aes-128-cbc -in flag.enc -out flag.txt -K $(echo -n "SuperSecret12" | xxd -p)  
iv undefined
```
I'm missing the IV. I found out that there is 2 "Default value" all 0 or the first 16 byte if the encrypted file


With trial and error it worked!
```bash
cat flag.txt 
4e4943437b53316d306e5f5472347633727365735f54316d337d
```
It took me an embarasing amount of time to figure out it was just the lfag in HEX

```
echo "4e4943437b53316d306e5f5472347633727365735f54316d337d" | xxd -r -p
NICC{S1m0n_Tr4v3rses_T1m3}
```

![alt text](img/toad.png)