# Finally, an un-strings-able problem
## Forensic
## Description
> I inherited this really cursed disk image recently. All the files seem to be corrupted and I can't even read some of them. What the heck is going on?

## Given 
- disk.img

# Solution

What do we have here?

```bash
file disk.img
disk.img: Linux rev 1.0 ext4 filesystem data, UUID=981eb2d5-0400-4c7d-986e-e9c3860666d3 (needs journal recovery) (extents) (64bit) (large files) (huge files)
```

Well lets mount that up!

```bash
sudo mount -o loop disk.img /mnt/unlock/
```

Lets explore those file

```bash
 ls -lah *.txt
--wx---rw- 1 root root 1.1K Mar 11 21:26 1Pe4S76zWpxA8mgI.txt
-rwxr--rwx 1 root root 1.1K Mar 11 21:51 3zkhN7A0Vqe0HgNC.txt
-rw---x-wx 1 root root 1.1K Mar 11 21:49 5UhgLeVLJWuEnc4W.txt
-rw---xr-- 1 root root 1.1K Mar 11 21:36 6ReSGoJsRnFqhg7r.txt
-r--rw-r-x 1 root root 1.1K Mar 11 21:50 B7HIyq5CKwGavwaW.txt
---xr-xr-- 1 root root 1.1K Mar 11 21:46 bG0d9OBnfwVP2NS8.txt
--wxr----- 1 root root 1.1K Mar 11 21:31 cDnYAOBE4mvBnh0C.txt
-rw--wx--x 1 root root 1.1K Mar 11 21:29 eiUFiXPDk6oee8sL.txt
-rwxr-xr-- 1 root root 1.1K Mar 11 21:35 fGMkb1gANtjLb5Qz.txt
-rwx--xr-- 1 root root 1.1K Mar 11 21:48 GeDYq3hoIx7oijhO.txt
-rwx--xr-- 1 root root 1.1K Mar 11 21:40 GP4decBqHC6UL66s.txt
-rw-rw---x 1 root root 1.1K Mar 11 21:53 HN5vsOJkU4004pEl.txt
-r-x---r-x 1 root root 1.1K Mar 11 21:34 HsxVbSgKw3d7tvFi.txt
----rw-r-x 1 root root 1.1K Mar 11 21:42 kcVtPjZM85b4B3V6.txt
--w---xr-- 1 root root 1.1K Mar 11 21:52 KEY19YZmg8L92D1H.txt
-r-xrwx--- 1 root root 1.1K Mar 11 21:30 kY4FOlfPt3qGR17K.txt
--wx-wxr-- 1 root root 1.1K Mar 11 21:39 LuVzAMVXkpJYAxRM.txt
----rw--wx 1 root root 1.1K Mar 11 21:38 lysJisb6wMlPG9WX.txt
-rw--w--wx 1 root root 1.1K Mar 11 21:33 OOVH70vCevC3FSZq.txt
--wxr-x-w- 1 root root 1.1K Mar 11 21:23 PtRcxoHyWhhS6z9q.txt
-r---wx-wx 1 root root 1.1K Mar 11 21:44 pU2aTHrPpCjthwwi.txt
-r--rw--wx 1 root root 1.1K Mar 11 21:25 R6qgmnljCORHERFH.txt
-rw---x-wx 1 root root 1.1K Mar 11 21:41 S5dyoQrp6a8grHOD.txt
-rwxr--rw- 1 root root 1.1K Mar 11 21:43 t7WeFKhvlS3e1Yet.txt
----r-xr-- 1 root root 1.1K Mar 11 21:27 u70m5b8l2T3vnZHZ.txt
----rwx--x 1 root root 1.1K Mar 11 21:37 uAkL5PqfK2I7K4PE.txt
--wx--xr-x 1 root root 1.1K Mar 11 21:32 Uljik5BaQPOeMjfc.txt
--wxrw--w- 1 root root 1.1K Mar 11 21:47 Vp7XQiTt4ad9IDfB.txt
-r-xrwxr-x 1 root root 1.1K Mar 11 21:54 W5xw54rLYvyj7qRM.txt
-rwx-wxrw- 1 root root 1.1K Mar 11 21:28 x9f1QlloTkYd5sfU.txt
-rwx-w---x 1 root root 1.1K Mar 11 21:24 y7Dsjz7CmkvpTA1H.txt
-r---wx-w- 1 root root 1.1K Mar 11 21:45 Z0VC73hFMVt2AcO9.txt
```

The file name and content seem in base 64, I played around with the content of the file.
Appending them in order of modified date, trying to decode their name, file carving name it... can't find any magic bytes

I came to the conclusion that they are garbage.

Then I did a `ls -la` and wow those permission are wacky...very wacky, `so octal encoding of the flag?`

Lets extract them in octal:
```bash
#!/bin/bash
directory="/mnt/unlock"
output_file="permissions_octal.txt"
> "$output_file"
find "$directory" -type f -name "*.txt" -exec stat --format="%Y %n" {} \; | sort -n | cut -d' ' -f2- |
while read file; do
    perms=$(stat -c "%a %n" "$file")
    echo "$perms" >> "$output_file"
done
```

Yield:

```
352 /mnt/unlock/PtRcxoHyWhhS6z9q.txt
721 /mnt/unlock/y7Dsjz7CmkvpTA1H.txt
463 /mnt/unlock/R6qgmnljCORHERFH.txt
306 /mnt/unlock/1Pe4S76zWpxA8mgI.txt
54 /mnt/unlock/u70m5b8l2T3vnZHZ.txt
736 /mnt/unlock/x9f1QlloTkYd5sfU.txt
631 /mnt/unlock/eiUFiXPDk6oee8sL.txt
570 /mnt/unlock/kY4FOlfPt3qGR17K.txt
340 /mnt/unlock/cDnYAOBE4mvBnh0C.txt
315 /mnt/unlock/Uljik5BaQPOeMjfc.txt
623 /mnt/unlock/OOVH70vCevC3FSZq.txt
505 /mnt/unlock/HsxVbSgKw3d7tvFi.txt
754 /mnt/unlock/fGMkb1gANtjLb5Qz.txt
614 /mnt/unlock/6ReSGoJsRnFqhg7r.txt
71 /mnt/unlock/uAkL5PqfK2I7K4PE.txt
63 /mnt/unlock/lysJisb6wMlPG9WX.txt
334 /mnt/unlock/LuVzAMVXkpJYAxRM.txt
714 /mnt/unlock/GP4decBqHC6UL66s.txt
613 /mnt/unlock/S5dyoQrp6a8grHOD.txt
65 /mnt/unlock/kcVtPjZM85b4B3V6.txt
746 /mnt/unlock/t7WeFKhvlS3e1Yet.txt
433 /mnt/unlock/pU2aTHrPpCjthwwi.txt
432 /mnt/unlock/Z0VC73hFMVt2AcO9.txt
154 /mnt/unlock/bG0d9OBnfwVP2NS8.txt
362 /mnt/unlock/Vp7XQiTt4ad9IDfB.txt
714 /mnt/unlock/GeDYq3hoIx7oijhO.txt
613 /mnt/unlock/5UhgLeVLJWuEnc4W.txt
465 /mnt/unlock/B7HIyq5CKwGavwaW.txt
747 /mnt/unlock/3zkhN7A0Vqe0HgNC.txt
214 /mnt/unlock/KEY19YZmg8L92D1H.txt
661 /mnt/unlock/HN5vsOJkU4004pEl.txt
575 /mnt/unlock/W5xw54rLYvyj7qRM.txt
```



Fixing permission and bit, as they are 4 digits. (I prefer working in python also)

```python
permissions_octal = [
    0o352, 0o721, 0o463, 0o306, 0o054, 0o736, 0o631, 0o570,
    0o340, 0o315, 0o623, 0o505, 0o754, 0o614, 0o071, 0o063,
    0o334, 0o714, 0o613, 0o065, 0o746, 0o433, 0o432, 0o154,
    0o362, 0o714, 0o613, 0o465, 0o747, 0o214, 0o661, 0o575
]

binary_string = "".join(f"{perm:09b}" for perm in permissions_octal)
print("Binary string:", binary_string)

bytes_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
flag = "".join(chr(int(b, 2)) for b in bytes_list if len(b) == 8)
print("Possible flag:", flag)
```

And rawr does the dinosaur

```bash
Binary string: 011101010111010001100110011011000110000101100111011110110011001101111000011100000011001101110010011101000101111101100110001100000111001000110011011011100111001100110001011000110101111100110100011011100011010001101100011110010111001100110001011100110101111100111010001100110110001101111101
Possible flag: utflag{3xp3rt_f0r3ns1c_4n4lys1s_:3c}
```

`utflag{3xp3rt_f0r3ns1c_4n4lys1s_:3c}`