# Trapped in Plain Sight 2
# Misc
## Description
> Only the chosen may see.

# Given
The password is password.
ssh -p REDACTED trapped@REDACTED

# Solution

We have this:

```bash
trapped@30ea1b120183:~$ ls -lah
total 36K
dr-xr-xr-x  1 trapped trapped 4.0K Mar 14 19:23 .
dr-xr-xr-x  1 root    root    4.0K Mar 14 19:23 ..
-r--r--r--  1 trapped trapped  220 Feb 25  2020 .bash_logout
-r--r--r--  1 trapped trapped 3.7K Feb 25  2020 .bashrc
-r--r--r--  1 trapped trapped  807 Feb 25  2020 .profile
----r-----+ 1 root    root      28 Mar 14 19:23 flag.txt
```

Notice the `+` on the flag permission? That mean ACL!

```bash
trapped@30ea1b120183:~$ getfacl flag.txt 
# file: flag.txt
# owner: root
# group: root
user::---
user:secretuser:r--
group::---
mask::r--
other::---
```

So secretuser can read the flag heh... lets check in /etc/passwd 

```bash
trapped@30ea1b120183:~$ cat /etc/passwd
[...]
secretuser:x:1001:1001:hunter2:/home/secretuser:/bin/sh
```

Wait.. wait.. did he really put the password in the GECOS field?

```bash
trapped@30ea1b120183:~$ su secretuser
Password: hunter2
$ cd /home/trapped
$ cat flag.txt
utflag{4ccess_unc0ntroll3d}
```

Yes he did...

`utflag{4ccess_unc0ntroll3d}`