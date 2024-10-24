# Dig The Container

# Flag 1: Ignored

Information:

- docker pull l3houx/projet_e
- ⚠️ IP sont fictive!!! Aucun besoins d'interagir avec autre qu'en "STRING" ⚠️

Donc.. euh on va aller chercher l'image et on rentre a l'interieur!

```bash
/projet-e # ls
IPs.json
/projet-e # cat IPs.json 
["70.13.37.224", "73.13.37.226", "78.13.37.181", "67.13.37.74", "84.13.37.186", "70.13.37.29", "45.13.37.95", "121.13.37.146", "111.13.37.87", "117.13.37.240", "95.13.37.145", "119.13.37.23", "97.13.37.191", "115.13.37.58", "95.13.37.171", "114.13.37.20", "105.13.37.101", "103.13.37.231", "104.13.37.116", "116.13.37.87", "95.13.37.74", "116.13.37.184", "104.13.37.138", "105.13.37.175", "115.13.37.13", "95.13.37.148", "119.13.37.12", "97.13.37.5", "115.13.37.164", "110.13.37.50", "116.13.37.52", "95.13.37.194", "111.13.37.80", "110.13.37.207", "108.13.37.126", "121.13.37.95", "95.13.37.220", "73.13.37.211", "80.13.37.128", "115.13.37.247"] 
```
```bash
/projet-e ls -lah
total 20K    
drwxr-xr-x    1 root     root        4.0K Aug  6 01:33 .
dr-xr-xr-x    1 root     root        4.0K Oct 24 21:40 ..
-rw-rw-r--    1 root     root         131 Aug  6 01:30 .dockerignore
drwxrwxr-x    8 root     root        4.0K Aug  6 01:33 .git
-rw-rw-r--    1 root     root         646 Aug  5 20:52 IPs.json
```

```bash
cat .dockerignore 
# RklOQ1RGe3lvdV9zb3VkbnRfa2VlcF9ldmVyeV9maWxlc19pbl9kb2NrZXJfaW1hZ2V9Cg==
Dockerfile
deploy_docker_image.sh
.env
#.git/
```

```bash
 echo RklOQ1RGe3lvdV9zb3VkbnRfa2VlcF9ldmVyeV9maWxlc19pbl9kb2NrZXJfaW1hZ2V9Cg== | base64 -d
FINCTF{you_soudnt_keep_every_files_in_docker_image}
```

Ouin, ok passons au prochain

# Flag 2: Git Gud
Bon le nom des challenges sont assez evocateur jusqu'a date

```bash
/projet-e git status
On branch main
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        deleted:    .gitignore
        deleted:    Dockerfile
        deleted:    deploy_docker_image.sh

/projet-2 git reset --hard
```
```bash
git log --all
f834ffa (HEAD -> main) Script de déploiement automatique de l'image Docker sur DockerHub
commit f834ffa486a13658ed50f867ef664d81d1d7217e (HEAD -> main)


    Oups! J'avais oublié le fichier des variables d'environnement.

commit c2efe897e44a4e99a6ae5d6da4c1a9618d7c4b48
Author: Elite H4x0r <EliteH4x0r@1337.ca>
Date:   Mon Aug 5 20:51:35 2024 -0400

    Ajout du fichier d'exclusions Git (gitignore)

commit f834ffa486a13658ed50f867ef664d81d1d7217e (HEAD -> main)
Author: Elite H4x0r <EliteH4x0r@1337.ca>
Date:   Mon Aug 5 20:50:04 2024 -0400

    Script de déploiement automatique de l'image Docker sur DockerHub

commit 961f4a5b4a60dcf9492daa7151160528f0836fde
Author: Elite H4x0r <EliteH4x0r@1337.ca>
Date:   Mon Aug 5 20:45:10 2024 -0400

    Créer le fichier de configurations Docker pour utiliser l'application dans un environnement contrôlé

commit ccb7388d4090666574312dd038f91b23f93bb7e3
Author: Elite H4x0r <EliteH4x0r@1337.ca>
Date:   Mon Aug 5 16:58:11 2024 -0400

    Ajout du JSON contenant des adresses IPs. Il y a quelque chose de louche dans ce fichier là...

commit 58b4ecebd4a7a6a85b78f1e3434a2424ed764e45
Author: Elite H4x0r <EliteH4x0r@1337.ca>
Date:   Mon Aug 5 16:56:49 2024 -0400

    Initial Commit

```

```bash
git checkout c2efe897e44a4e99a6ae5d6da4c1a9618d7c4b48
 cat .env
#RklOQ1RGLWhtbW1fbmVpdGhlcl9wdXNoX2V2ZXJ5dGhpbmdfdG9fZ2l0Cg==
DOCKER_USERNAME="USERNAME"
DOCKER_PASSWORD="PASSWORD"
```

```bash
echo RklOQ1RGLWhtbW1fbmVpdGhlcl9wdXNoX2V2ZXJ5dGhpbmdfdG9fZ2l0Cg== | base64 -d
FINCTF-hmmm_neither_push_everything_to_git
```

# Flag 3:👁️🫛

Encore une fois le nom est evocateur jetons un oeil au IP
```json
["70.13.37.224", "73.13.37.226", "78.13.37.181", "67.13.37.74", "84.13.37.186", "70.13.37.29", "45.13.37.95", "121.13.37.146", "111.13.37.87", "117.13.37.240", "95.13.37.145", "119.13.37.23", "97.13.37.191", "115.13.37.58", "95.13.37.171", "114.13.37.20", "105.13.37.101", "103.13.37.231", "104.13.37.116", "116.13.37.87", "95.13.37.74", "116.13.37.184", "104.13.37.138", "105.13.37.175", "115.13.37.13", "95.13.37.148", "119.13.37.12", "97.13.37.5", "115.13.37.164", "110.13.37.50", "116.13.37.52", "95.13.37.194", "111.13.37.80", "110.13.37.207", "108.13.37.126", "121.13.37.95", "95.13.37.220", "73.13.37.211", "80.13.37.128", "115.13.37.247"]
```
⚠️ Elle sont fictive ⚠️

Elle semble a premiere vue toute valide. L'indice que je n'ai pas regarder lors du CTF pointe vers la table ascii (https://www.asciitable.com/).
Donc, est-ce que cela serais une chaine encoder?.. dans un CTF? sa n'arrive jamais... voyon

```python

ip_list = [
    "70.13.37.224", "73.13.37.226", "78.13.37.181", "67.13.37.74", "84.13.37.186", "70.13.37.29",
    "45.13.37.95", "121.13.37.146", "111.13.37.87", "117.13.37.240", "95.13.37.145", "119.13.37.23",
    "97.13.37.191", "115.13.37.58", "95.13.37.171", "114.13.37.20", "105.13.37.101", "103.13.37.231",
    "104.13.37.116", "116.13.37.87", "95.13.37.74", "116.13.37.184", "104.13.37.138", "105.13.37.175",
    "115.13.37.13", "95.13.37.148", "119.13.37.12", "97.13.37.5", "115.13.37.164", "110.13.37.50",
    "116.13.37.52", "95.13.37.194", "111.13.37.80", "110.13.37.207", "108.13.37.126", "121.13.37.95",
    "95.13.37.220", "73.13.37.211", "80.13.37.128", "115.13.37.247"
]

def decode_message(ip_list):
    flag = ""
    for ip in ip_list:
        ascii_code = int(ip.split('.')[0])
        flag += chr(ascii_code)
    return flag

my_flag = decode_message(ip_list)
print("Here is your flag goodsir:", my_flag)
print("And moreover, have a nice day")
```

```bash
python decode.py 
Here is your flag goodsir: FINCTF-you_was_right_this_wasnt_only_IPs
And moreover, have a nice day
```
![alt text](img/image.png)