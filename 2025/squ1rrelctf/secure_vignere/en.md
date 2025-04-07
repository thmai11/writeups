# Secure Vignere
## Crypto
## Solver: CombatWorthyWombat


we are given the following instruction:

"Connect to: nc 20.84.72.194 5007 Wrap the flag with squ1rrel{}"

when we do that we are greeted with:

========================================

Welcome! Here's the flag! It's just encrypted with a vigenere cipher with a random key!
The key is a random length, and I randomly picked letters from "squirrelctf" to encrypt the flag!
With so much randomness there's no way you can decrypt the flag, right?
Flag: mxpqmlslzrrhwoaellqfraiukjnmzv

========================================

**initial thoughts:**

we are told it is vignere, ∴ len(plaintext) == len(ciphertext)
	- len(ciphertext) = 30
	- ∴ flag is 30 chars
unfortunatley, we are told that we need to wrap the flag with "squ1rrel{}" - so no chosen plaintext attacks can be used

each time we connect to the server, we are given a different encryption;
	- the key is of random length every time ∴ we cant be sure when len(key) < len(plaintext)
	- the characters of the key are random every time, but chosen from "squirrelctf"
		- re-using chars must be allowed to allow for random length keys,
		- so: "rrrrrrrrrrrrrrrrrrrrrrrrrrrrr" could be a valid key
	- assume random weighting for characters ∴ "r" has a 'weight' of 2
	- and all other chars have a weight of 1
	
given infinite possible encryptions (that we can access) what could we expect, pattern wise,
that might give us a clue as to the plaintext?

index of coincidence only applies if we find encryptions where len(key) < len(plaintext)
(which we can't be sure about)

worst case scenario is if len(key) >= len(plaintext) = >= 30
	- each character has a p(1/11) chance of being: [s, q, u, i, e, l, c, t, f]
	- and a p(2/11) chance of being: [r]
	
for each char; 10 different options ∴ for length 30, 10^30 options - or one thousand billion billion billion
	- assuming good code, at 300 billion operations/second
	- 1/3 x 10^19 seconds -> 95070000000 years
	- ∴ we need a more efficient algorithm than guessing the worst case scenario
	- or we assume a best key length scenario

hmm, lets try looking for some patterns
if we query the server 10000 times, we'd get a list of ciphertexts:

ct x: mxpqmlslzrrhwoaellqfraiukjnmzv
ct y: njroknsmxssixpbfmkrgsbjvlkomaw
ct z: oypqlotnzttjyqcgnlshtckwmnlobx

as vignere uses rotation, if a character in the ciphertexts match,
we know the character in the key at that position is also the same

also - as [a] is not in [s, q, u, i, e, l, c, t, f], the plaintext cannot be ROT0
∴ every character in the plaintext cannot be found in any ciphertext at the same position

say the key is:

ky 1: fffffffffffffffffffffffffffffs

ky 2: rrrrrrrrrrrrrrrrrrrrrrrrrrrrrs
then:

ct 1: ?????????????????????????????x

ct 2: ?????????????????????????????x

the rotations of [s, q, u, i, e, l, c, t, f] and [r] are: [+18, +16, +20, +8, +4, +11, +2, +19, +6, +17]

so we can create a possible characters list for that final character
which (if we found matching pairs with "x") are:
[x+18, x+16, x+20, x+8, x+4, x+11, x+2, x+19, x+6, x+17]
[p, n, r, f, b, i, z, q, d, o]

========================================

**possible weakness:**

not all of the characters in the key have equal appearance value
∴ given we have sufficiently many ciphertexts, for a given char position:
	- there will be 10 different resulting chars
	- of those, 9 will have an equal p(1/11) chance of occuring
	- 1 will have a p(2/11) chance of occuring - this will correspond to rot[26-17] of that character
	
over a large enough sample of ciphertexts
we can decrypt that one character with some certainty

**∴ plan is:**

========================================

get lots of ciphertexts, and anaylse one set position across them ->
find the frequency distribution of those 10 possible characters at that position ->
if there are enough to assume a decently random distribution ->
assume the character corresponding to a p(2/11) frequency is rotated by [r] ->
undo the rotation by doing ROT[26-17] ->
perform this for each of the 30 character slots in the flag length ->
wrap the flag

p(r being selected) = 1 - (1 - p)^n
so say we aim for 99.99% certainty:
0.9999 = 1 - (1 - 2/11)^n
(1 - 2/11)^n = 0.0001
n = 45.89...

99.99% certainty requires =^= 46 cases
95% certainty requires =^= 20 cases

lets aim for 1000 cases, just to be sure:

========================================
```
# Created on Tue April 06
# Python 3
# UTF-8
# @author: CWW

# generating 100 encrypted responses dictionary

import socket

host = "20.84.72.194"
port = 5007

def netcat(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # connect to the server
    server_response = client_socket.recv(1024)  # save the response to a variable
    client_socket.close()  # close the socket after receiving the data
    return server_response

def parse(server_response):
    trimmed_response = server_response[264:]
    trimmed_response = trimmed_response[:30]
    trimmed_response = trimmed_response.decode('utf-8')
    return trimmed_response
    # takes the response and trims it to just the 30 characters of the encrypted vigenere

def retrieve_ciphertext():
    vignere_enc = netcat(host, port)
    x = parse(vignere_enc)
    return x
    # function to pin the above together - its a little messy i know

if __name__ == "__main__":
    
    output_file = "vignere_encrypted_dictionary.txt"
    
    with open(output_file, 'w') as f:  # open file in write mode
        for i in range(1, 1001):
            ciphertext = retrieve_ciphertext()
            f.write(ciphertext + '\n')  # write each output to a new line in the file
            print(ciphertext)  # print to console for my visual sanity
```		
========================================

this gives us a dictionary file to work with
now for a solve script:

========================================
```
# Created on Sun April 6th
# Python 3
# UTF-8
# @author: CWW

# vignere solver for squirrel CTF - using a dictionary of saved encryptions

from collections import Counter
from rdout import rdout, style

def analyze_frequencies(file_path):
    # create a list of counters for each character position
    position_counters = [Counter() for _ in range(30)]
    
    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            for i, char in enumerate(line):
                if i < 30:
                    position_counters[i][char] += 1
                 
    for i, counter in enumerate(position_counters):
        rdout(style.GREEN, f"position {i + 1}:")
        for char, count in counter.items():
            print(f"  {char}: {count}")
        print()
    return position_counters

def assemble_common_chars(position_counters):
    vignere_string = ""
    rdout(style.GREEN, "most frequent character positions:")
    for i, counter in enumerate(position_counters):
        if counter:
            most_common = counter.most_common(1)[0]
            print(f"{i + 1}: {most_common[0]} (freq: {most_common[1]})")
            vignere_string += most_common[0]
        else:
            break
    
    rdout(style.BLUE, "vigenere string: ")
    print(vignere_string)
    return vignere_string

def rot(string, rotation):
    result = []
    
    for char in string:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        if char in alphabet:
            start = ord('a')
            rotated_char = chr((ord(char) - start + rotation) % len(alphabet) + start) # modular rotation
            result.append(rotated_char)
    rotated_string = ''.join(result)        
    rdout(style.BLUE, "rotated vignere string:")
    print(rotated_string)
    return rotated_string

file_name = "vignere_encrypted_dictionary.txt"
position_counters = analyze_frequencies(file_name)
vignere_string = assemble_common_chars(position_counters)
rot(vignere_string, (26-17))
```
========================================

this gives us the string: ithoughtrandomizationwassecure

wrap and we have the flag: sqrl{ithoughtrandomizationwassecure}