
# ECB
## Crypto

# Solved by @CombatWorthyWombat

This writeup and solve are completely made by CombatWorthyWombat!
I edited the formatting to suit markdown format.


# we are given the following:

"Everyone keeps telling me how ECB isn't meta-viable and that I should stop playing it to tournaments.
Well, I love ECB so I've added some new tech that should hopefully get me some better results!"

By Sasha (@kyrili on discord)
nc REDACTED 7150

as well as a "main.py"


the title; Espathra-Csatu-Banette - seems to be something to do with pokemon TCG
the blurb adds to that flavour, could be relevant, or could just be another acronym for ECB

looking at the python code first impressions:

```
AES using ECB mode
imports "key" from a static address -> (key)
imports "flag.txt" from a static address -> (secret)
it then encodes the (secret):
AES encode using cipher module: AES.new(key. AES.MODE_ECB)
this generates the value for variable: (cipher) - which is just a normal AES ECB of a static key and message pair

then it gets a little whacky, a sort of custom oracle is used:
the server script requests user input ->(x)
it then runs a custom checksum function on (x):
checksum = sum(ord(c) for c in x) mod (len(x)+1)
checksum = (sum of ascii values of all characters in (x)) mod (length of (x) +1)
```

it then constructs a new "plaintext" (pt) by inserting the flag: (secret) checksum characters along the user supplied (x)

```
say for instance, (x) = help

the sum of all the ascii chars for hello is:
72 + 101 + 108 + 80
= 361
length of (x) + 1:
len(hello) = 4
len(hello) + 1 = 5
checksum:
361 mod 5
= 1
```
then the (pt) "new plaintext generator" would create:

hutflag{???}elp

by inserting "utflag{???}" 1 character along our (x)
```
==========================================
it then generates a ciphertext (ct) from this new plaintext (pt)
uses PKCS7 padding, which adds the value of (16-(trailing byes)) to each remaining to make full 16 byte blocks
==========================================
```
Oracle + ECB + the ability to prefix = padding attack

we can force the flag to be prefixed with 31 bytes to force the first char into the previous block:

[AAAAAAAAAAAAAAAA][AAAAAAAAAAAAAAAu][tflag{??????????]

as any given plaintext will encode to the same ciphertext, we can guess ASCII characters untill we get a match
this takes our possible guess space from: 16^73 -to-> 1^73

we encrypt:

[AAAAAAAAAAAAAAAA][AAAAAAAAAAAAAAAu]

and the two encrypted blocks should match the oracle's from the previous encryption

[df5d902adeebcf264ca316e20ee9b26c][e9306fab95a6440c56fe8ed58c81a807]
[df5d902adeebcf264ca316e20ee9b26c][e9306fab95a6440c56fe8ed58c81a807]

as both match we know the flag's first character is "u"


inputting our own plaintext is made a little more complex with the "chksm" function:
```
	chksum = sum(ord(c) for c in x) % (len(x)+1)
	pt = x[:chksum] + secret + x[chksum:]
```

so I made a small function to generate a string that would prefix the flag with a chosen plaintext and insert point:
```python
===========================================
import itertools

def checksum(string, target_checksum):
    charsum = sum(ord(char) for char in string)
    charlen = len(string) + 1
    checksum_value = charsum % charlen
    if checksum_value == target_checksum:
        print(f"Checksum for {string} = {checksum_value} (or: {charsum} mod {charlen})")
        return True
    return False

def search_for_matching_checksum(start_string, target_checksum):
    allowed_char_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-~!?#%&@{}"
    match_count = 0
    for length in range(len(start_string), len(start_string) + 10):
        for comb in itertools.product(allowed_char_list, repeat=length - len(start_string)):
            new_string = start_string + ''.join(comb)
            if checksum(new_string, target_checksum):
                match_count += 1
                if match_count == 1:
                    return (new_string)

if __name__ == "__main__":
    
    start_string = input("Enter the start string: ")  
    target_checksum = int(len(start_string))
    search_for_matching_checksum(start_string, target_checksum)
===========================================
```

this allows me to craft any prefix I want for the oracle to encrypt

after a long time, and referencing:
https://gist.github.com/bricef/f6e39b09dc0e9f7c287fdab0beb66545
https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py

i managed to get a piece of code to work!:

```python
===========================================
# -*- coding: utf-8 -*-
"""
@author: CWW
"""

from pwn import *
import itertools
from enum import Enum

MAX_FLAG_LEN = 128

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-~!?#%&@{}"
# formatting
# ===========================================================================
class colour(Enum): 
    GRAY = '\033[30m' 
    RED = '\033[31m' # Use for failed attempts
    GREEN = '\033[32m' # Use for successful attempts
    YELLOW = '\033[33m' # Use for partial failed attempts
    BLUE = '\033[34m' # Use for information
    PURPLE = '\033[35m' # Use for errors
    TEAL = '\033[36m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
def rdout(colour, string):
    print(colour.value, "==========================================================", colour.RESET.value, sep="")
    print(colour.BOLD.value, string, colour.RESET.value, sep="")
    print(colour.value, "==========================================================", colour.RESET.value, sep="")
# ===========================================================================

# functions
# ===========================================================================
def checksum(string, target_checksum):
    charsum = sum(ord(char) for char in string)
    charlen = len(string) + 1
    checksum_value = charsum % charlen
    if checksum_value == target_checksum:
        print(f"Checksum for {string} = {checksum_value} (or: {charsum} mod {charlen})")
        return True
    return False

def search_for_matching_checksum(start_string, target_checksum):
    match_count = 0
    for length in range(len(start_string), len(start_string) + 10):
        for comb in itertools.product(alphabet, repeat=length - len(start_string)):
            new_string = start_string + ''.join(comb)
            if checksum(new_string, target_checksum):
                match_count += 1
                if match_count == 1:
                    return (new_string)

def ecb_byte_construct(known_plaintext=""):
    known_plaintext = ("A" * 16) + known_plaintext

    def read_ciphertext():
        ciphertext = int(process.readline().decode(), 16)
        ciphertext = ciphertext.to_bytes(length=(ciphertext.bit_length()+7)//8, byteorder="big")
        return ciphertext

    for i in range(MAX_FLAG_LEN):
        padding = 15 - (i % 16)
        plaintext = search_for_matching_checksum(("A" * padding), len("A" * padding))
        process.sendlineafter(b"to be encrypted: ", plaintext.encode())
        ciphertext = read_ciphertext()

        dict_ciphertexts = {}
        for c in alphabet:
            dict_known_plaintext = known_plaintext[len(known_plaintext)-16+1:len(known_plaintext)]
            dict_plaintext = search_for_matching_checksum(dict_known_plaintext + c, len(dict_known_plaintext + c))
            process.sendlineafter(b"to be encrypted: ", dict_plaintext.encode())
            dict_ciphertexts[c] = read_ciphertext()

        block_to_attack = (padding + i) // 16
        ciphertext_block_to_attack = ciphertext[block_to_attack * 16: (block_to_attack + 1) * 16]

        for c in alphabet:
            matching_chars = True
            for j in range(16):
                if ciphertext_block_to_attack[j] != dict_ciphertexts[c][j]:
                    matching_chars = False
                    break

            if matching_chars:
                known_plaintext += c
                rdout(colour.GREEN, "flag so far: " + (f"{known_plaintext[16:]}"))
                break

        if "}" in known_plaintext:
            return known_plaintext[16:]

if __name__ == "__main__":
    
    flag = ecb_byte_construct(known_plaintext="utflag{")
    rdout(colour.GREEN, ("flag: " + flag))
===========================================
```
the flag ends up being:

`utflag{st0p_r0ll1ng_y0ur_0wn_crypt0!!}`