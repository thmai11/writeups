# Treasure hunt

### Information:
- docker.io/unshade/what


Its in container category. So i go check the image on the official registry

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

So far `RUN /bin/sh -c echo "Part 1 of flag: 4T\${d0ck3r" > /home/ctfuser/.secret_note # buildkit`

I try to get a shell in it... and i dosnt work?
Gathering information about the image:

``` bash
docker image inspect unshade/what
#[...]
"Architecture": "arm64",
#[...]
```

Ohhh, `qemu` can help me here, brb installing some more lib
After a couple command and test

```bash
docker run --platform linux/arm64 -it unshade/what /bin/sh
```

I'm in so lets take a look at `app.py`

`Part 2 of flag: _1s_fun}`

Treasure:

`4T${d0ck3r_1s_fun}`

And X mark the spot