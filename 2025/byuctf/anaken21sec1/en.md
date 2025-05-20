# Crypto
## Solved by `@CombatWorthyWombat` [https://github.com/CombatWorthyWombat](Github)

#### Edited for markdown format

We are given the following:
- a key: "orygwktcjpb"
- an encrypted flag: "cnpiaytjyzggnnnktjzcvuzjexxkvnrlfzectovhfswyphjt"
- a note reminding us to wrap the flag in "byuctf{}"
- and  a "encrypt.py" file

# First impressions

thought the name might imply something - but i think its just the author's name

the encryption function is as follows:

		def encrypt(plaintext, key):
			plaintext += "x"*((12-len(plaintext)%12)%12)
			blocks = [plaintext[12*i:12*(i+1)] for i in range(0,len(plaintext)//12)]
			keyNums = [ord(key[i])-97 for i in range(len(key))]
			resultLetters = ""

			
lots of clipping the encryption into 12 length pieces, maybe some sort of block cipher?
	- can confirm some sort of block cipher, the following code padds the input pt to be ≅ 0 mod(12)
		- plaintext += "x"*((12-len(plaintext)%12)%12)
		
then it splits the padded plaintext into 12 length blocks

the next piece turns each character of the key into a number, from 0 to 25, where [a = 0] and [z = 25]

interestingly, the key gen function cannot generate a key with the letter "z":

		def getRandomKey():
			letters = "abcdefghijklmnopqrstuvwxy"
			key = choice(letters)
			for i in range(1,11):
				oldletter = key[i-1]
				newletter = choice(letters)
				oldletterNum = ord(oldletter)-97
				newletterNum = ord(newletter)-97
				while (newletterNum//5 == oldletterNum//5 or newletterNum%5 == oldletterNum % 5) or newletter in key:
					newletter = choice(letters)
					newletterNum = ord(newletter)-97
				key+=newletter
			return key
			
I suspect this is in order to map well onto a 5x5 matrix, of which there are 5 of the following format:

		A = np.array([[1, 7, 13, 19, 25, 31],
					[2, 8, 14, 20, 26, 32],
					[3, 9, 15, 21, 27, 33],
					[4, 10, 16, 22, 28, 34],
					[5, 11, 17, 23, 29, 35],
					[6, 12, 18, 24, 30, 36]])
					
I think all the newkey oldkey stuff is just key formatting - which doesn't matter for us as we just have the key
unless its avoiding some sort of scenario with adjacent numbers that we will come across later



## Steps seem to be:


key is generated of length 11
- no two adjacent letters in the key share a row or column if they were arranged in a 5x5 grid based on their ord - 97
plaintext is sanitized:
- all non letter chars are removed
- uppercase are converted to lowercase
- padding is added to ensure the len(pt) ≅ 0 mod(12)
the plaintext is now split into blocks of length 12
within each block, the characters are converted to a 6x6 matrix (called blockM)
- each letter is converted to a number where [a = 1] and [z = 26]
- then i think each letter-number is split into a three digit base three number (not sure though)
- the first 6 letters occupy rows 0->2:
- the next 6 occupy rows 3->5:
	
        A1 B1 C1 D1 E1 F1 G1
        A2 B2 C2 D2 E2 F2 G2
        A3 B3 C3 D3 E3 F3 G3
        H1 I1 J1 K1 L1 M1 N1
        H2 I2 J2 K2 L2 M2 N2
        H3 I3 J3 K3 L3 M3 N3
	
- where A1,A2,A3 are the three base 3 digits that correspond to the character "A" in the key the matrix is then altered
	- convert each character of the key to a digit where [a = 0] and [z = 25]
	- reorder the matrix using one of the 5 provided arrays [A, B, C, D, E]
	- perform modifications on the matrix numbers
		- increment some matrix numbers
		- add some matrix numbers to eachother
		- all these are taken modulo 3 to keep them within base 3

the matrix is then converted to characters
- the groups of three numbers are combined into a single number using [9*a + 3*b + c]
- this maps to a character using the number retrieved + 96, such that "a" -> ord("a")


these ciphertext characters are then rearranged according to the key - a sort of transpositional cipher
- we reuse the keynums from before, a list of numbers corresponding to the key characters where [a = 0] and [z = 25]
- any duplicate numbers are then removed and stored as reducedkeynums
- for each item in the reducedkeynums, a list is created and the letters of the ct are arranged among them as follows:
- say our ct is ["abcdefghij"]
    - lets say our keynums is [3, 1, 2, 1]
    - reducedkeynums is therefore [3, 1, 2]
    - for each item in reducedkeynums, we make an empty list, [] [] []
    - each letter in the ct is assigned to a list cyclically where you end up splitting the ct into 'columns'

            letterbox0 = ["a", "d", "g", "j"]
            letterbox1 = ["b", "e", "h"]
            letterbox2 = ["c", "f", "i"]
		
		- we get the index of the smallest item in reducedkeynums and then set it to 27
		- as 27 is outside our search range of 26 alphabetical characters, this places marks it as "used"
			- so for [3, 1, 2]
			- we find the smallest item, 1
			- find its index, which is 1
			- then replace it with 27 -> [3, 27, 2]
		- the index we found is then used to rearrance the ciphertext characters from before
		- the letterboxes represent 'rows', and we take our index and find the row corresponding to letterbox [index]
			- in this case, letterbox[1] = ["b", "e", "h"]
		- the items in this letterbox are put together to make our final ciphertext string so;
		for keynums [3, 1, 2, 1] -> reducedkeynums [3, 1, 2]
		
        ```
        letterbox0 = ["a", "d", "g", "j"]
        letterbox1 = ["b", "e", "h"]
        letterbox2 = ["c", "f", "i"]
		
        1st index: [3, 1, 2] -> [3, 27, 2] = 1
        2nd index: [3, 27, 2] -> [3, 27, 27] = 2
        3rd index: [3, 27, 27] -> [27, 27, 27] = 0
		```
		so we take letterbox[1, 2, 0] and append them
		
		ciphertext = ["behcfiadgj"]


so i guess the first step is working out what our keynums and reducedkeynums are for our given key

ciphertext = `"cnpiaytjyzggnnnktjzcvuzjexxkvnrlfzectovhfswyphjt"`

key = `"orygwktcjpb"`
so `keyNums = [14, 17, 24, 6, 22, 10, 19, 2, 9, 15, 1]`

as there are no repeated numbers in the key;
reducedKeyNums = `[14, 17, 24, 6, 22, 10, 19, 2, 9, 15, 1]`

the final indexing step would have gotten the following values:
`[10, 7, 3, 8, 5, 0, 9, 1, 6, 4, 2]`

as the reducedKeyNum is length 11, there would be 11 letterboxes, and our ciphertext is length 48

48/11 = 4 remainder 4.

so, each letterbox had 4 characters minimum, and the first 4 had an extra letter in each

	letterbox0  [5 chrs]
	letterbox1  [5 chrs]
	letterbox2  [5 chrs]
	letterbox3  [5 chrs]
	letterbox4  [4 chrs]
	letterbox5  [4 chrs]
	letterbox6  [4 chrs]
	letterbox7  [4 chrs]
	letterbox8  [4 chrs]
	letterbox9  [4 chrs]
	letterbox10 [4 chrs]

```
the first index value is 10, so the first [4 chrs] of the ciphertext are the contents of letterbox10
aytjyzggnnnktjzcvuzjexxkvnrlfzectovhfswyphjt
index 7 -> [4 chrs]
yzggnnnktjzcvuzjexxkvnrlfzectovhfswyphjt
index 3 -> [5 chrs]
nnktjzcvuzjexxkvnrlfzectovhfswyphjt
index 8 -> [4 chrs]
jzcvuzjexxkvnrlfzectovhfswyphjt
index 5 -> [4 chrs]
uzjexxkvnrlfzectovhfswyphjt
index 0 -> [5 chrs]
xkvnrlfzectovhfswyphjt
index 9 -> [4 chrs]
rlfzectovhfswyphjt
index 1 -> [5 chrs]
ctovhfswyphjt
index 6 -> [4 chrs]
hfswyphjt
index 4 -> [4 chrs]
yphjt
index 2 -> [5 chrs]
```

the reconstructed letterboxes are as follows:

    0  [u, z, j, e, x]
    1  [r, l, f, z, e]
    2  [y, p, h, j, t]
    3  [y, z, g, g, n]
    4  [h, f, s, w]
    5  [j, z, c, v]
    6  [c, t, o, v]
    7  [a, y, t, j]
    8  [n, n, k, t]
    9  [x, k, v, n]
    10 [c, n, p, i]

reconstructed ciphertext (pre transposition):

`"uryyhjcanxczlpzfztynknjfhgscotkvpezjgwvvjtnixetn"`

=========================================================================	

im pretty confident in the de-transposition step - now to do the next piece (which i wont do by hand i think xD)

for the [permute] and [add] functions ill try make an opposite [reverse permute] and [reverse add]

		def permute(blockM, count):                                             <- takes "blockM", a numpy array and "count", which selects which permutes from the list to use
			finalBlockM = np.zeros((6,6))                                       <- creates an empty 6x6 matrix
			for i in range(6):                                                  <- iterates over all the "rows"
				for j in range(6):                                              <- iterates over all the "columns"
					index = int(permutes[count][i,j]-1)                         <- takes an index (0 -> 35 for each of the positions in the matrix)
					finalBlockM[i,j] = blockM[index//6, index%6]                <- takes index values and converts them to coordinates (using floor division and modulo)
			return finalBlockM                                                  <- returns the new block

we still use the same function inputs (we'll handle block splitting later)
the index line we can keep the same - as we want the same item in the matrix that would have undergone permutation to undergo reverse permutation

the encrypt 

		def reverse_permute(blockM, count):
			finalBlockM = np.zeros((6,6))
			for i in range(6):
				for j in range(6):
					index = int(permutes[count][i,j]-1)
					finalBlockM[index//6,index%6] = blockM[i,j]                 <- swap the previous instructions and retrieve the pre-permuted block
			return finalBlockM

now for the reverse_add function, this is the normal one:

		def add(blockM, count):                                                 <- takes as args "blockM", a 6x6 numpy array, and "count", which is the key derived value that chooses whic of the permutes to use
			if count == 0:                                                      <- if we choose the 1st permute
				for i in range(6):                                                 -> for each of the 6 rows
					for j in range(6):                                             -> and each of the 6 columns
						if (i+j)%2 == 0:                                           -> if their sum is even
							blockM[i,j] +=1                                        -> increase their value by 1
			elif count == 1:                                                    <- if count points to the 2nd permute
				blockM[3:,3:] = blockM[3:,3:]+blockM[:3,:3]                     <- add the bottom right quadrant of the matrix to the top left quadrant
			elif count == 2:                                                    <- if count points to the 3rd permute
				blockM[:3,:3] = blockM[3:,3:]+blockM[:3,:3]                     <- add the top left quadrant of the matrix to the bottom right quadrant
			elif count == 3:                                                    <- if count points to the 4th permute
				blockM[3:,:3] = blockM[3:,:3]+blockM[:3,3:]                     <- add the bottom left quadrant of the matrix to the top right quadrant
			else:                                                               <- else (count points to the 5th permute)
				blockM[:3,3:] = blockM[3:,:3]+blockM[:3,3:]                     <- add the top right quadrant of the matrix to the bottom left quadrant
			return np.mod(blockM, 3)                                            <- reduce all values to fit base 3, so [0, 1, 2]
			
hmm, actually - i dont need to reverse all of this, just the one piece that our key codes to
so the count variable is defined (took me ages to find for some reason):

		blockM = add(blockM, keyNum % 5)

the "count" variable is the [keyNum % 5] piece
given we already have our keyNum from earlier:

we know: so keyNums = [14, 17, 24, 6, 22, 10, 19, 2, 9, 15, 1]

        for keyNum in keyNums:
            blockM = permute(blockM,(keyNum//5)%5)
            blockM = add(blockM, keyNum%5)
			
ahh - nevermind, we have to do it for each num in keyNums, so we might as well reverse the whole add function
here's the reversed function (we can keep all the permute counts):

		def reverse_add(blockM, count):                                          <- same args as before
			if count == 0:                                                       <- for count 0 or 1st permute
				for i in range(6):                                                  -> for each of the 6 rows
					for j in range(6):                                              -> and for each of the 6 columns
						if (i + j) % 2 == 0:                                        -> if the sum of the column and row indicies is even
							blockM[i, j] -= 1                                       -> decrease their value by 1
			elif count == 1:                                                     <- for count 1
				blockM[3:,3:] = (blockM[3:,3:] - blockM[:3,:3]) % 3              <- subtract top left from bottom right staying in the modular space for base 3
			elif count == 2:                                                     <- for count 2
				blockM[:3,:3] = (blockM[:3,:3] - blockM[3:,3:]) % 3              <- subtract bottom right from top left in mod 3
			elif count == 3:                                                     <- for count 3
				blockM[3:,:3] = (blockM[3:,:3] - blockM[:3,3:]) % 3              <- subtract top right from bottom left mod 3
			else:                                                                <- for count 4
				blockM[:3,3:] = (blockM[:3,3:] - blockM[3:,:3]) % 3              <- subtract bottom left from top right mod 3
			return np.mod(blockM, 3)                                             <- make sure its all mod 3 (for the addition step which can yield -1)
			
so to finnish, we have to just assemble the other smaller pieces:

we have our hardcoded values;
- the permutes from the encryption script
- the keyNums we did earlier while figuring out the encryption
- our de-transposed ciphertext
- the key given in the challenge
	
we have our reversed functions;
- reverse_add
- reverse_permute
- reversed scrambler/count finder
- removing "x" (the padding character) from the end of the readout
	
the functions that stay the same;
- base 3 to base 10 converter
- building the blocks

# Solution:

combining all this we get:

```python
			import numpy as np

			# permutes from the encryption script
			A = np.array([[1, 7, 13, 19, 25, 31],
						[2, 8, 14, 20, 26, 32],
						[3, 9, 15, 21, 27, 33],
						[4, 10, 16, 22, 28, 34],
						[5, 11, 17, 23, 29, 35],
						[6, 12, 18, 24, 30, 36]])
			B = np.array([[36, 30, 24, 18, 12, 6],
						[35, 29, 23, 17, 11, 5],
						[34, 28, 22, 16, 10, 4],
						[33, 27, 21, 15, 9, 3],
						[32, 26, 20, 14, 8, 2],
						[31, 25, 19, 13, 7, 1]])
			C = np.array([[31, 25, 19, 13, 7, 1],
						[32, 26, 20, 14, 8, 2],
						[33, 27, 21, 15, 9, 3],
						[34, 28, 22, 16, 10, 4],
						[35, 29, 23, 17, 11, 5],
						[36, 30, 24, 18, 12, 6]])
			D = np.array([[7, 1, 9, 3, 11, 5],
						[8, 2, 10, 4, 12, 6],
						[19, 13, 21, 15, 23, 17],
						[20, 14, 22, 16, 24, 18],
						[31, 25, 33, 27, 35, 29],
						[32, 26, 34, 28, 36, 30]])
			E = np.array([[2, 3, 9, 5, 6, 12],
						[1, 11, 15, 4, 29, 18],
						[7, 13, 14, 10, 16, 17],
						[20, 21, 27, 23, 24, 30],
						[19, 8, 33, 22, 26, 36],
						[25, 31, 32, 28, 34, 35]])
			permutes = [A, B, C, D, E]

			# hardcoded keyNums from ye olde manual part earlier
			keyNums = [14, 17, 24, 6, 22, 10, 19, 2, 9, 15, 1]

			# our de-transposed ciphertext
			ciphertext = "uryyhjcanxczlpzfztynknjfhgscotkvpezjgwvvjtnixetn"

			# our key
			key = "orygwktcjpb"

			# reversed matrix permute function
			def reverse_permute(blockM, count):
				inverse = np.zeros((6, 6))
				for i in range(6):
					for j in range(6):
						index = int(permutes[count][i, j] - 1)
						inverse[index // 6, index % 6] = blockM[i, j]
				return inverse

			# reversed matrix add function
			def reverse_add(blockM, count):
				if count == 0:
					for i in range(6):
						for j in range(6):
							if (i + j) % 2 == 0:
								blockM[i, j] -= 1
				elif count == 1:
					blockM[3:,3:] = (blockM[3:,3:] - blockM[:3,:3]) % 3
				elif count == 2:
					blockM[:3,:3] = (blockM[:3,:3] - blockM[3:,3:]) % 3
				elif count == 3:
					blockM[3:,:3] = (blockM[3:,:3] - blockM[:3,3:]) % 3
				else:
					blockM[:3,3:] = (blockM[:3,3:] - blockM[3:,:3]) % 3
				return np.mod(blockM, 3)

			def decrypt(ciphertext, key):
				blocks = [ciphertext[i:i+12] for i in range(0, len(ciphertext), 12)]
				plaintext = ""

			# reversed block handler
				for block in blocks:
					blockM = np.zeros((6, 6))
					for i in range(6):
						letter = block[i]
						num = 0 if letter == "0" else ord(letter) - 96
						blockM[i, 0] = num // 9
						blockM[i, 1] = (num % 9) // 3
						blockM[i, 2] = num % 3
					for i in range(6):
						letter = block[i+6]
						num = 0 if letter == "0" else ord(letter) - 96
						blockM[i, 3] = num // 9
						blockM[i, 4] = (num % 9) // 3
						blockM[i, 5] = num % 3
						
			# reversed count finder
					for keyNum in reversed(keyNums):
						blockM = reverse_add(blockM, keyNum % 5)
						blockM = reverse_permute(blockM, (keyNum // 5) % 5)
						
			# for the 36 base 3 matrix numbers to base 10 ints
					for i in range(6):
						num = int(9 * blockM[0, i] + 3 * blockM[1, i] + blockM[2, i])
						if num == 0:
							continue
						plaintext += chr(num + 96)
					for i in range(6):
						num = int(9 * blockM[3, i] + 3 * blockM[4, i] + blockM[5, i])
						if num == 0:
							continue
						plaintext += chr(num + 96)

				return plaintext.rstrip("x")

			if __name__ == "__main__":
				print(decrypt(ciphertext, key))
				
```

when we run this we get:

`revisreallythestartingpointformostcategoriesiydk`

wrapping the flag we get:
`byuctf{revisreallythestartingpointformostcategoriesiydk}`

that one was tricker than I thought, my coding skills need a little work

\- CWW