# Whispers of the Forgotten
# Forensic
# Description:
> Lost echoes of the past await those who can see beyond the surface, revealing secrets hidden in the void.

# Given
- a memdump of a windows VM

# Solution

Ok this one I have been trolled HARD. I found trace of a ransomware and a BUNCH of fake flag..
In the end I solved it with... `strings`....

```bash
strings memdump.mem | grep pastebin
```

In all the link this one: https://pastebin.com/zk0wH7Pj
`apoorvctf{ur1s_n3v3r_1i3}`

