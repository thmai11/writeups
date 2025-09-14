# A star is born
## Misc

## Description
```
My friend has always dreamed of being a rockstar. Unfortunately, he's always been a poor musician. But do you know what my friend is really good at? Working with AI.
He sent me his latest composition and mentioned that he hid a little surprise in it. Can you figure out what he hid?
```


We have an mp3 file.
Inspecting it with binwalk

```bash
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             MP3 ID3 tag, v2.3
3809408       0x3A2080        Zip archive data, encrypted at least v2.0 to extract, compressed size: 521, uncompressed size: 1295, name: lyric.txt
3810091       0x3A232B        End of Zip archive, footer length: 22
```

Extracting it with `binwalk -e` we retrieve the zip file.
Since it is password protected we must find the password.

In exif we have the following: `Album                           : MW10aDNwNHNzdzByZA==`
The password is encoded in b64: `1mth3p4ssw0rd`

We find `lyric.txt` which contain rockstar code
You can either install it or using : `https://codewithrockstar.com/online`

The program yield : `100 114 103 110 123 121 48 117 114 101 95 116 104 51 95 114 48 99 107 115 116 97 114 125` which are ASCII code
Using: `https://codebeautify.org/ascii-to-text` or simple python script

It yield: `drgn{y0ure_th3_r0ckstar}`

