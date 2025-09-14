# Title: pd_what
## Forensics

## Description
```
Here is a fun little PDF I found! I added a flag into it, nothing special, just a good old zip file. But, will you be able to read it in this very limited environment? Open it with a Chromium-based browser like Chrome if you want it to work! I am not the author of the original project.

Archive password: 12345
Flag Format: drgn{.*}
Author: drgn
```

# Solution
The goal of this challenge is just extracting the data of flag.zip from the pdf then cracking it with john and rock you.

When I found this little project: https://github.com/ading2210/linuxpdf
I though it would be cool to make a challenge with it :). Props to the author!

Flag in actually encoded in the PDF in b64 then compressed with zlib
Its the embedded_file `0000000000000003`

```python
import base64
import zlib

data_b64 = "eNoL8GZm4WLgZGBguNLtFyUgJvrLGMhWB2IOBhmGtJzEdL2SipLQEE4GZv4j69NBuLSCm4GR5QUzAwOY0PaLqi6NWtiV6Bz96NwL8SkJM6JearDrTOg/N7vuwNGN8zj7r+4/1Cp64jjvfMu1l3gLJiddC/Bm50C2KsCbkUmOGZczJBhAgBGIlzSCWAhHsUIcheagAG9WNogORgY/IN0K1g8A9Io6rg=="  
data_compressed = base64.b64decode(data_b64) 
data = zlib.decompress(data_compressed) 


with open('flag.zip', 'wb') as f:
    f.write(data) 
```


It yield flag.zip as output.bin

Just crack it

```bash
zip2john flag.zip > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt 
# flag.zip/flag.txt:Braxton78:flag.txt:flag.zip::flag.zip
unzip -x flag.zip
cat flag.txt
# drgn{l1nux_0n_4_pdf??_1'v3_s33n_1t_4ll}
```

# Pit fall
Most of the contestant did not zlib-decompress the file thus were unable to crack using rockyou database :(