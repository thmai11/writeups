# Leaky Stream
# Forensic
# Description
> In the middle of our conversation, some packets went amiss. We managed to resend a few but they were slightly altered. Help me reconstruct the message and I'll reward you with something useful ;)

# Given
- pcap file

# Solution
I solved this one very easily with the help of strings
```
strings chitty-chat.pcapng | grep -i VishwaCTF
VishwaCTF{this_is_first_part
```
```
strings chitty-chat.pcapng | grep -i }
\Device\NPF_{4F0C51D2-BC6F-4BA4-B390-207D4F49F697}
_this_second_part}
[...]
```

Then i spent 30min trying to understand how it worked! Well i learned something that packet in wireshark can have comment?!

![alt text](img/pcap.png)

`VishwaCTF{this_is_first_part_this_second_part}`