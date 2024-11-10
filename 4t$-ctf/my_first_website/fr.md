# My first website

### Information

⚠️ Ceci est un challenge de type blue-team. Il n'y a pas de flag, mais plutot une requete qui est envoyer sur le serveur afin de valider que la vulnerabilité à été corrigé.

- webshell
- http://REDACTED


En regardant dans les dossiers de `nginx` j'ai trouver que l'authentification était assuré par `.htaccess`

```
admin:$apr1$ylTvWSmW$YKsO3kx3XCS.7OT0ExXFm.
```

Je le crack donc avec `john` et `rockyou.txt`
```bash
john --show hash.txt 
admin:admin
```

Aw... oh... effectivement ce n'est pas très sécuritaire -_-'

```bash
htpasswd .htpasswd admin
```

admin:NEW_SECURE_PASSWORD?

Je demande une validation et .... solved!