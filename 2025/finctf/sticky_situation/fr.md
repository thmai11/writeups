# Sticky Situation

## Catégorie: Forensic
## Description:

>On m’a dit d’arrêter de coller mon mot de passe de production sur un post-it sur le tableau d’affichage à côté de mon bureau… mais c’est tellement pratique.
>Je crois que j’ai trouvé une autre façon de le stocker — de toute façon, ils ne peuvent pas accéder à mon ordinateur, non ?

Format du flag
`FINCTF{.*}`

## Solution

Nous avons donc:
```bash
file memdump.mem
memdump.mem: data
```

Pour naviguer dans les dumps memoire volatility est un tres bon outil
[Cheasheet Volatility](https://blog.onfvp.com/post/volatility-cheatsheet/)

Il faut comprendre que le flag est dans le Program `Sticky Note` de windows.
Il n'est pas installer par default et c'est le seul program qui a ete installer sur cette VM.

Les sticky note sauvegarde leur donner dans plum.sqlite
```
vol -f memdump.mem windows.filescan | grep -i plum.sqlite
0xc482c3c75330.0\Users\drgn\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite-wal
0xc482c3c7a150  \Users\drgn\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite
0xc482c3c82df0  \Users\drgn\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite-shm
```

Donc avec le module filedump et les addresses memoires, il est possible de recupere ces fichiers!

La base de donnee SQLite est presentement vide car les donnee sont dans le checkpoint sqlite-wal, on peut les flusher dans le fichier avec
```bash
echo "PRAGMA wal_checkpoint(TRUNCATE);" | sqlite3 plum.sqlite
```

On peut maintenant trouver le contenue des sticky note:
```sql
sqlite3 plum.sqlite "select * from Note"
\id=fff1588b-64ee-425e-9e34-f06bb5d21f28 Timmy, rapelle-toi de ceci: 7S-?B<(;3lFEM)/?SQG*D)6#_Ed<'|ManagedPosition=DeviceId:\\?\DISPLAY#Default_Monitor#4&17f0ff54&0&UID0#{e6f07b5f-ee97-4a90-b076-33f57bf4eaa7};Position=654,186;Size=320,320|1|0||Yellow|0||||||0||1514e413-5fc1-4260-aa33-09cd59401225|72d96a4f-ab62-49ed-8918-5accead29112|638968492477501600||638968503868277838
```

Le contenue de la note: `Timmy, rapelle-toi de ceci: 7S-?B<(;3lFEM)/?SQG*D)6#_Ed<'`

`7S-?B<(;3lFEM)/?SQG*D)6#_Ed<'` correspond a `FINCTF{5tuck_1n_m3m0ry}` en base85

Sticky Situation: `FINCTF{5tuck_1n_m3m0ry}`

P.S. Timmy est en hommage au celebre developpeur web de l'entreprise Desgazons