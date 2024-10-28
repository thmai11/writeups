# memory-puzzle

# Description

```
The Consortium has concealed a critical file within a memory dump, protected by layers of digital obfuscation. Led by Simon Letti, participants must sift through the volatile memory landscape to locate a plaintext key that unlocks the encrypted file. Time is of the essence, as Roko's Basilisk threatens to distort the data with each passing moment. Can you unravel the puzzle before the Basilisk intervenes?

"Basilisk's whisper will not wait" echos through your mind as you enter the file.

(Note: If you choose to use volatility2.6, use profile Win10x64_19041)
```
Fichier `memory-puzzle.rar`

## Developpe par Trent (https://github.com/tkg1121)

Deja on nous parle de volatility, je ne le connaissais pas et ce sera un bon ajout dans ma boite a outil!

⚠️ J'utiliserai Volatility 3 durant ce writeup

Contenue de l'archive
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

J'ai donc fais un dump avec volatility 3 des choses suivantes:
(Une chance que j'ai egalement trouver ceci! https://blog.onfvp.com/post/volatility-cheatsheet/ )
- `windows.pstree`
- `windows.filescan`

Ceci a attirer mon attention!
```
*** 1980        4976    notepad.exe     0xb1084122e080  5       -       1       False   2024-10-18 06:43:38.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\notepad.exe    "C:\Windows\system32\NOTEPAD.EXE" C:\Users\johndoe\Desktop\system_update.py     C:\Windows\system32\NOTEPAD.EXE
```
On a donc un utilisateur `johndoe` qui editais le fichier `C:\Users\johndoe\Desktop\system_update.py` avec `C:\Windows\system32\NOTEPAD.EXE` ainsi que sont PID et PPID!
Avec le retour de volatility sur le `windows.filescan`

```bash
cat file_scan_output | grep johndoe
[...]
# Beaucoup de fichier mais surtout ces 2 la qui attire mon attention
0xb1083fcf40c0  \Users\johndoe\Desktop\system_update.py
0xb1084089e960  \Users\johndoe\Desktop\system_update.exe
[...]
```
Je tente donc faire un `windows.dumpfiles` sur ces 2 fichiers

```bash
vol -f memory_puzzle.raw -o files/ windows.dumpfiles --virtaddr 0xb1083fcf40c0 # system_update.py virt adddress
vol -f memory_puzzle.raw -o files/ windows.dumpfiles --virtaddr 0xb1084089e960 # system_update.exe virt adddress
```

- system_update.py: Aucun retour de volatility
- system_update.exe: Extrait le fichier!

Quel est ce fichier?
```bash
file file.0xb1084089e960.0xb1083edb4550.DataSectionObject.system_update.exe.dat
file.0xb1084089e960.0xb1083edb4550.DataSectionObject.system_update.exe.dat: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c094c53ae90b55cff2d739824790963e767852f0, for GNU/Linux 3.2.0, not stripped
```

Strings?
```bash
# Je garde ici uniquement ceux d'interet
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

Ok ! Je comprend assez rapidement que la cle est en 2 partit,
- SuperSecH
- retKey12H

Que l'encryption est `aes-128-cbc`, que simplement voir `OPENSSL_3.0.0` me mentionne que je peux surement utilisee `openssl`
Donc la cle semble etre `SuperSecretKey12` le H signifie qu'il est en hexadecimal

Hey bien allons-sy!
```bash
openssl enc -d -aes-128-cbc -in flag.enc -out flag.txt -K $(echo -n "SuperSecret12" | xxd -p)  
iv undefined
```
Aw... il me manque donc le IV. Je cherche alors et je trouve ces 2 "default value"  `0*16` ou les premier 16 bit du fichier 

Pour finalement 
```bash
cat flag.txt 
4e4943437b53316d306e5f5472347633727365735f54316d337d
```
Sa ma pris un peu de temps a comprendre que c'est simplement le flag en HEX

```
echo "4e4943437b53316d306e5f5472347633727365735f54316d337d" | xxd -r -p
NICC{S1m0n_Tr4v3rses_T1m3}
```

![alt text](img/toad.png)