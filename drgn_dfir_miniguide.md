# Forensic
I got often asked if I could write a guide for forensic, this is kinda though as I think this category often named as "misc" can throw at you the most wacky and obscur things.
⚠️ I did not proof read this, and did not put a lots of time into this. So excuse my poor writing ⚠️

## Stego
General rules for stego is to figure out what the *** am I dealing with. `file` command might tell you, sometime its just `data` 
If file dosnt tell you what it is... then probably the author manipulated the file signature or magic byte.

Open ImHex and verify file signature (it has probably been tampered with) https://en.wikipedia.org/wiki/List_of_file_signatures

### Image
Start by using `strings`, `exiftool` and `binwalk/foremost` as carving tool 

⚠️ Don't get baited by the zlib part of png file. Those by nature are zlib compressed of course a file carver will notice the compressed data

#### PNG:
Try this: https://github.com/DominicBreuker/stego-toolkit with all tools that support png. 
You can use the bash script included with the container
- check_png.sh 
- brute_png.sh with rockyou or custom wordlist
There is an equivalent with
- check_jpg.sh
- brute_jpg.sh with rockyou or custom wordlist

(IMHO this is better than aperisolve)

IF anything failed use ImHex and validate that the PNG dosnt have any extra data and stuff with the patterned view

You can also verify the integrity (CRC check and stuff) with `pngcheck -v file`

#### JPG:
Same as PNG, but JPG are way harder you can try 
    - DCT coeffificient graph

To verify jpg you can use `JPGSNOOP (windows)`

#### Other Format or if all the above fail (Hint that happen real often)
When everything "simple" failed it might be a corrupted img file so check the file format and `analyse the hex code`
What ive seen often
  - is all the marker which are suposed to `UPPERCASE` have been switched in `lowercase`
  - byte reordering like as an exempple:

```
89 50 4E 47 0D 0A 1A 0A # Those are the PNG header
50 89 47 4E 0A 0D 0A 1A # Those were the byte in the given file

I just wrote a python script that undo that operation on the whole file and tada... fixed png which was containing the flag
```
Exemple: https://github.com/thmai11/writeups/blob/main/2025/apoorvctf/samurai_code/en.md

Don't forget those can be "visual" one I ALWAYS run `stegoveritas` on and it catched up a few low hanging fruit

#### Library
Most of the time you will resolve to write a python script so learn to use those library:
- pillow
- scikit-image

Saves a shit ton of time. Ask GPT about it, but when GPT spit me out some code, I always have to modify it to suit my need on the particular challenge.

### MP3:
Check with `audacity in spectrogram view` maybe there something hidden in there
Check for embedded `file with carving tool binwalk/foremost`
Also check with `exiftool` as mp3 have some `metadata like album, artist and stuff` where you can hide thing
Then check usuall audio stego tool like `DeepSound` again linking this: https://github.com/DominicBreuker/stego-toolkit 

### MIDI:
Check for the same as MP3 but understand that midi arent compresse like mp3. So you have more possibilities to hide stuff
Check all the track with an appropriate software
Some stuff could be hidden in frequencies 

### SVG:
SVG are XML file https://github.com/thmai11/writeups/blob/main/2024/spookyctf/wont-somebody-think-of-the-children/en.md

### Audio in general
Audio file might encode the flag in the content.. could be melody, frequence of sound, name it. Really depend on the challenge

### PDF:
Pdf is a VERY open format.. https://github.com/ading2210/linuxpdf
Learn to use:
- qpdf

And there is way more lib to verify PDF but most of the time I open them as plain text. There could be binary object in them and I saw many challenge that you had to just recombine them

### Text Stego
Know that stegsnow exists, so if you find a bunch of tab and space... might be stegsnow

### Conclusion for stego:
Always verify that some kind of password or key are not given somewhere in the challenge. Those are mandatory to solve it so... don't push it too far on LSB 
Don't forget about `Binarization` sometime when you can clearly identify two "type of value" in a given challenge could be just...
- Sound above and under 1000MhZ resolve to `1` and `0`
- The measure of a cube in blender yield to be `1` and `0` for a QR Code: https://github.com/thmai11/writeups/blob/main/2025/apoorvctf/blend_in_disguise/en.md

Here one that had a few stego step: https://github.com/thmai11/writeups/blob/main/2025/ehax/tracks/en.md

## PCAP
Oh those pcap, you will love to hate them

Learn to use:
- wireshark
- tshark (often data still need more transformation so you output them to a file a write a script to solve it)
- pyshark (sometime easier by just source the pcap and pyshark allow you to do this)

### TCP
- Probably a LOTS of traffic, you need to narrow down which packet are relevant
`Wireshark`: Go in `Statistics -> Conversation`
You will see who speaks to who which is VERY usefull to isolate conversation in all those paquet

Also there is probably encryption be sure to get those key exchange (verify on the internet how it work on the paquet depending which type of encryption there is)
If found, inject them into wireshark to be able to filter on those now unencrypted packet!

#### HTTP, FTP, File transfering case
`Wireshark`: `File -> Export` object and select the protocol sometime you can extract file sent that are not encrypted
For `HTTP` verify which url has been queried and of course inspect the requests made!


### USB
First thing first `IDENTIFY` what device you are facing.
- Keyboard? Get those HID and convert them back to ASCII what did the user typed?
- Headphone or any audio device? Extract the sounds and listen to it! (https://github.com/thmai11/writeups/blob/main/2025/apoorvctf/broken_tooth/en.md)
etc..etc..etc..

### ICMP
ICMP type 8 are ping.. there should not be 64k of data into that...

### Final note on PCAP
Don't neglect `string` ever, EVER
https://github.com/thmai11/writeups/blob/main/2025/vishwactf/leaky_stream/en.md

## Memdump
Those are my favorite!
Did I say never don't run a `strings` check on a file? https://github.com/thmai11/writeups/blob/main/2025/apoorvctf/whisper_of_the_forgotten/en.md

- volatility3
- volatillity2.X

You WILL need a valid python2 installation
vol3 is SO MUCH EASIER TO USE.. but vol2.X have MANY plugings you WILL need both trust me
Use pyenv for managing python version and venv https://github.com/pyenv/pyenv saves a LOTS of time

Use this cheatsheet https://blog.onfvp.com/post/volatility-cheatsheet/ but ⚠️ ⚠️ ⚠️ DO NOT COPY THE COMMAND, when copied it don't work in my console -_-'
Vol3 plugin: https://github.com/spitfirerxf/vol3-plugins
Vol2 plugin: https://github.com/volatilityfoundation/community

I usually run vol and send all the output to a file, then i open it as CSV with VScode and the rainbow CSV pluging it help searching thing
pslist.csv
pstree.csv
cmdline.csv
etc..etc..etc..

Where to look really depend on the challenge.. might be in browser history, browser password vault... very very challenge dependent...
Usually it involved malware so get a sandbox ready. A windows VM should be more than enough for isolation. 
Well... if you can write a malware that can get out of a VM plz ping me and I will buy your code ;)

## Diskdump
Those are fun. 
First Never, never don't run a `strings`: https://github.com/thmai11/writeups/blob/main/2025/kashictf/memories_bring_back_you/en.md
(Try the base64 or some other variant. Just drop the padding `==` in you're grep)

Now, 
- FTK Imager
- Autopsy
- photorec
- Good old linux

Check
- deleted file
- Alternate data stream
- vshadow for windows dump
- partition or any other kind of stuff in the metadata

Mount that god damn thing if needed! Its easy on linux to mount block device ask GPT about it (installing maor library incomming for obscur thing)
QEMU is also you're friend if you actually need to run something 

## Esoteric language
Learn to recognize those wacky programming language
- brainfuck
- whitespace
- rockstar
- meowlang
- LOLCODE
- https://en.wikipedia.org/wiki/Esoteric_programming_language

# Final note: 
You will face the most random and wacky stuff in Forensic... general rule of thumb
1. Identify what you are looking for
2. Get the Data required
3. Script it to victory

Farewell traveller