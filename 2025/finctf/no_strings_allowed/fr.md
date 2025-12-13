# No-Strings-Allowed
# Catégorie: Forensic / Divers

Description:

> Parfois, je résous des challenges forensic complexes... avec strings... l’auteur a oublié d’encoder son flag. Ce n’est pas le cas ici : strings ne pourra pas t’aider !

Format du flag:
`FINCTF{.*}`



# Flag: FINCTF{fl4g_1n_0ct4l!!}
# Flag Octal: 106 111 116 103 124 106 173 146 154 64 147 137 61 156 137 60 143 164 64 154 41 41 175

# Recon

On a un donc
```bashv
disk.img: Linux rev 1.0 ext2 filesystem data, UUID=abb16da5-9311-4e70-8770-ee94ef7e1253, volume name "flag_img" (extents) (64bit) (large files) (huge files)
```

Parfait une image linux! On fais quoi avec cela?...

On le monte
```bash
sudo mount -o loop,ro disk.img /flag
```
Le filesysteme contient des fichier flag_[0-22] qui sont tous vide...
Mais dans un systeme de fichier il y a d'autre donnee, comme... des permissions...

```bash
ls -lah
Permissions Size User Group Date Modified Name
.--x---rw-     1 root root  24 Oct 17:10  flag_0
.--x--x--x     1 root root  24 Oct 17:10  flag_1
.--x--xrw-     1 root root  24 Oct 17:10  flag_2
.--x----wx     1 root root  24 Oct 17:10  flag_3
.--x-w-r--     1 root root  24 Oct 17:10  flag_4
.--x---rw-     1 root root  24 Oct 17:10  flag_5
.--xrwx-wx     1 root root  24 Oct 17:10  flag_6
.--xr--rw-     1 root root  24 Oct 17:10  flag_7
.--xr-xr--     1 root root  24 Oct 17:10  flag_8
.---rw-r--     1 root root  24 Oct 17:10  flag_9
.--xr--rwx     1 root root  24 Oct 17:10  flag_10
.--x-wxrwx     1 root root  24 Oct 17:10  flag_11
.---rw---x     1 root root  24 Oct 17:10  flag_12
.--xr-xrw-     1 root root  24 Oct 17:10  flag_13
.--x-wxrwx     1 root root  24 Oct 17:10  flag_14
.---rw----     1 root root  24 Oct 17:10  flag_15
.--xr---wx     1 root root  24 Oct 17:10  flag_16
.--xrw-r--     1 root root  24 Oct 17:10  flag_17
.---rw-r--     1 root root  24 Oct 17:10  flag_18
.--xr-xr--     1 root root  24 Oct 17:10  flag_19
.---r----x     1 root root  24 Oct 17:10  flag_20
.---r----x     1 root root  24 Oct 17:10  flag_21
.--xrwxr-x     1 root root  24 Oct 17:10  flag_22
```

Ces permissions me semble tres suspicieuse 🤔
Les permissions sont en octal... et si on regardais leur valeur en ASCII?

```
#!/bin/bash
directory="/flag"
output_file="permissions_octal.txt"
> "$output_file"
find "$directory" -type f -exec stat --format="%Y %n" {} \; | sort -n | cut -d' ' -f2- |
while read file; do
    perms=$(stat -c "%a %n" "$file")
    echo "$perms" >> "$output_file"
done
```

Une fois trier,

```
106 /flag/flag_0
111 /flag/flag_1
116 /flag/flag_2
103 /flag/flag_3
124 /flag/flag_4
106 /flag/flag_5
173 /flag/flag_6
146 /flag/flag_7
154 /flag/flag_8
64 /flag/flag_9
147 /flag/flag_10
137 /flag/flag_11
61 /flag/flag_12
156 /flag/flag_13
137 /flag/flag_14
60 /flag/flag_15
143 /flag/flag_16
164 /flag/flag_17
64 /flag/flag_18
154 /flag/flag_19
41 /flag/flag_20
41 /flag/flag_21
175 /flag/flag_22
```

On le decode en ASCII
```python
permissions_octal = [
    0o106, 0o111, 0o116, 0o103, 0o124, 0o106, 0o173, 0o146, 0o154, 0o64,
    0o147, 0o137, 0o61, 0o156, 0o137, 0o60, 0o143, 0o164, 0o64, 0o154,
    0o41, 0o41, 0o175
]

flag = ''.join(chr(p & 0xFF) for p in permissions_octal)
print("Flag:", flag)
```

No-Strings-Allowed: `FINCTF{fl4g_1n_0ct4l!!}`

