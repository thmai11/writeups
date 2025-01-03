# Treasure hunt

### Information:
- docker.io/unshade/what


Premièrement dans la catégorie docker j'aime bien aller voir les informations

```dockerfile
ADD file:702193928cded0bcec5edbf4a5660961e7caef8c9d9cafea3337b7f6720c4464 in / 
CMD ["bash"]
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LANG=C.UTF-8
RUN /bin/sh -c set -eux; 	apt-get update; 	apt-get install -y --no-install-recommends 		ca-certificates 		netbase 		tzdata 	; 	rm -rf /var/lib/apt/lists/* # buildkit
ENV GPG_KEY=REDACTED
ENV PYTHON_VERSION=3.9.20
ENV PYTHON_SHA256=REDACTED
RUN /bin/sh -c set -eux; 	...REDACTED...	
RUN /bin/sh -c set -eux; 	...REDACTED...
CMD ["python3"]
RUN /bin/sh -c mkdir -p /app/data # buildkit
WORKDIR /app
RUN /bin/sh -c echo "Nothing to see here..." > /app/data/file1.txt &&     echo "Try harder!" > /app/data/file2.txt &&     echo "Getting warmer..." > /app/data/hidden.txt # buildkit
COPY app.py app.py # buildkit
RUN /bin/sh -c useradd -m ctfuser # buildkit
RUN /bin/sh -c echo "ctfuser:password123" | chpasswd # buildkit
RUN /bin/sh -c echo "Part 1 of flag: 4T\${d0ck3r" > /home/ctfuser/.secret_note # buildkit
RUN /bin/sh -c chown -R ctfuser:ctfuser /home/ctfuser # buildkit
CMD ["python", "app.py"]
```

Déjà: RUN /bin/sh -c echo "Part 1 of flag: 4T\${d0ck3r" > /home/ctfuser/.secret_note # buildkit

Je tente de rentré à l'intérieur: cela ne fonctionne pas.... ?!
Je cherche un peu d'information sur l'image 

``` bash
docker image inspect unshade/what
#[...]
"Architecture": "arm64",
#[...]
```

Ohhh, `qemu` peut me venir en aide donc j'install quelque lib!
Après quelque tests:

```bash
docker run --platform linux/arm64 -it unshade/what /bin/sh
```

Voila! je suis a l'intérieur et je vais voir directement le code python `app.py`

`Part 2 of flag: _1s_fun}`

Donc...

`4T${d0ck3r_1s_fun}`

