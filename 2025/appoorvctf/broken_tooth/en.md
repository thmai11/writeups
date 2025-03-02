# Broken Tooth
# Forensic
# Description:
> My buddy Blackbeard with a Broken Blue Tooth keeps preaching about being a sigma, but I caught him vibing to some pookie music. I've captured the packets, help me bully him by identifying the song.
Flag Format: apoorvctf{artist-song}
Example: Never Gonna Give You Up - by Rick Astley
Flag: apoorvctf{rick_astley-never_gonna_give_you_up}

# Given
- pcap file

So we have a bluetooth device. We need to extract the audio from it (As stated by the challenge flag format)
First lets get only the interesting data:

```bash
tshark -r Blackbeard.pcapng -d "btl2cap.cid==0x0043,bta2dp" -T json -x > data.json
```

With this simple script we extract the sbc data

```python
import json

j = json.loads(open("data.json").read())

sbc_frames = [ _ for _ in [i["_source"]["layers"].get("sbc_raw") for i in j] if _ is not None ]

print(len(sbc_frames))

data = "".join(frame[0][2:]for frame in sbc_frames)

open("something.sbc","wb").write(bytes.fromhex(data))
```

Now lets put that into a wav with ffmepg:

```bash
ffmpeg -i something.sbc flag.wav
```

You can see the file in assets/flag.wav

Now I just heard the lyric and searched then up 

https://genius.com/Billie-eilish-birds-of-a-feather-lyrics

```
Birds of a feather, we should stick together, I know
I said I'd never think I wasn't better alone
Can't change the weather, might not be forever
But if it's forever, it's even better
``` 
Indeed match what I hear

`apoorvctf{billie_eilish-birds_of_a_feather}`