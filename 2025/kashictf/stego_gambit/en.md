# Stego Gambit
## Forensic

## Description
> Do you dare to accept the Stego Gambit? I know you can find the checkmate but the flag!!

# Solved by @blackth0rns

We have the following:

![alt text](img/chall.jpg)

In exif:
```bash
ExifTool Version Number         : 10.40
File Name                       : chall.jpg
Directory                       : .
File Size                       : 48 kB
File Modification Date/Time     : 2025:02:22 12:14:18+00:00
File Access Date/Time           : 2025:02:23 18:55:46+00:00
File Inode Change Date/Time     : 2025:02:22 16:26:08+00:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : Use the moves as a key to the flag, separated by _
Image Width                     : 817
Image Height                    : 815
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 817x815
Megapixels                      : 0.666
```

`Use the moves as a key to the flag, separated by _`

I'm not a chess player so I had to go to https://nextchessmove.com/?fen=8/8/8/8/1K6/2P5/k5Q1/2R4B%20w%20-%20-%200%201
I came to the conclusion that the next moves are:

- white: Bh1
- black: Kxa2 (only move available)
- white: Qg2
- black: checkmate

___

# Now here is where my teamate come to the rescue

In chess 1 "move" is each player taking turn
So move 1 is:
- Bh1Kxa2
- Qg2#

`#` means checkmate

So our key to the stego is `Bh1Kxa2_Qg2#`

Now its time to play the good old classic : Which stegp technique/tool was use !

Fortunately it was a common one:

```bash
root@b97cabd99531:/data# steghide extract -sf chall.jpg -p "Bh1Kxa2_Qg2#"
wrote extracted data to "flag.txt".
root@b97cabd99531:/data# cat flag.txt 
KashiCTF{573g0_g4m617_4cc3p73d}
```

`KashiCTF{573g0_g4m617_4cc3p73d}`

![alt text](img/gambit.png)