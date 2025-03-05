# Phantom Connection
# Description:
> Like a fleeting dream, a connection once existed but has faded into the void. Only shadows of its presence remain. Can you bring it back to light?

# Forensic

# Given
- bcache24.bmc
- Cache0000.bin

# Solution

First we got to know what kind of file this is
```bash
file *
bcache24.bmc:  empty
Cache0000.bin: data
```
Ok yeah, so lets google that

https://github.com/ANSSI-FR/bmc-tools

`bmc-tools processes bcache*.bmc and cache????.bin files found inside Windows user profiles.`

Lets try that, it yield a bunch of file

```bash
file *
[...]
Cache0000.bin_1979.bmp: PC bitmap, Windows 95/NT4 and newer format, 64 x 48 x 32, cbSize 12410, bits offset 122
```
Oh ok those are image, after looking at them those came out of interest:


![alt text](img/Cache0000.bin_1791.bmp)
![alt text](img/Cache0000.bin_1790.bmp)

`apoorvctf{CAcH3_Wh4T_YoU_sE3}`
