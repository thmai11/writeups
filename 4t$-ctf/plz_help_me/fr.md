# Plz help me

### Information

⚠️ Ceci est un challenge de type blue-team. Il n'y a pas de flag, mais plutot une requete qui est envoyer sur le serveur afin de valider que la vulnerabilité à été corrigé.

- webshell
- On nous informe que le serveur redémarre tous les 10min

Je pense donc tout de suite a 2 chose
- cron
- systemd timer

En fouillant je retrouve ceci: `/usr/lib/systemd/system/cleanup.service`
J'ai également trouver un fichier `cleanup.sh` dans le file system `/opt`

Il fait un `eval` du résultat d'un `GET http://commander:5000` 
J'ai fais des appels au URL et 
- shutdown -h now

Et quelque autre commande bidon pour ecrire de faux flag.

En continuant à fouiller au niveau du `$PATH` je trouve que cleanup.sh est également dans `/bin` ou `/usr/bin` et que je peux l'écrire!
(Il y a également un commentaire disant de supprimer le contenue du fichier et d'effectuer le tests pour avoir le flag)

`vi` ou `nano` n'est pas disponible donc

```bash
echo > /bin/cleanup.sh
```

Quelque minute après la copie dans `/opt` a été remplacé par celle dans `/bin` 

Ceci était la correction!