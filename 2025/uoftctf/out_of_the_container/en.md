# Out of the container

## Description 
Testing out a new program I wrote on the cloud! docker pull windex123/config-tester

## Solution 
Getting the container

`docker pull windex123/config-tester:v1`

Its an ARM architecture. I already have qemu so lets analyse the layer as running it dosnt seem to do anything

![alt text](img/dive1.png)

Lets dump the layer with

`docker save windex123/config-tester:v1 -o config-tester.tar`

Only the json is relevant, the other one is a text file with `hey i'm a config` or something like that

```json
{
  "type": "service_account",
  "project_id": "uoftctf-2025-docker-chal",
  "private_key_id": "REDACTED",
  "private_key": "-----BEGIN PRIVATE KEY-----\nREDACTED-----\n",
  "client_email": "docker-builder@uoftctf-2025-docker-chal.iam.gserviceaccount.com",
  "client_id": "112040922998091528251",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/docker-builder%40uoftctf-2025-docker-chal.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

We can use this to connect to the GCP platform.

There was some container images 

This one was interesting:

`dive us-east1-docker.pkg.dev/uoftctf-2025-docker-chal/containers/countdown-test:latest`

![alt text](img/dive2.png)

https://github.com/OverjoyedValidity/countdown-timer/blob/main/settings.txt

`uoftctf{out-of-the-bucket3}`

# FUN!

I notice another project

```bash
gcloud projects list                                                                                                                                                                                           
PROJECT_ID                NAME                      PROJECT_NUMBER
helical-arcade-447510-s7  My First Project          651249475447
uoftctf-2025-docker-chal  uoftctf-2025-docker-chal  234692588405
```

```bash
gcloud storage buckets list                                                                                                                                                                                    
---
creation_time: 2025-01-12T10:29:15+0000
default_storage_class: STANDARD
generation: 1736677754630505664
location: US
location_type: multi-region
metageneration: 1
name: helical-arcade-447510-s7-daisy-bkt-us
public_access_prevention: inherited
rpo: DEFAULT
soft_delete_policy:
  retentionDurationSeconds: '0'
storage_url: gs://helical-arcade-447510-s7-daisy-bkt-us/
uniform_bucket_level_access: true
update_time: 2025-01-12T10:29:15+0000
```

I'm in a CTF and i'm not quite sure what I was looking for at this point so...

```bash
gsutil cp -r gs://helical-arcade-447510-s7-daisy-bkt-us/daisy-image-export-ext-20250112-10:30:04-v1nn7/ .
```

```
file export-disk                                                             
export-disk: VMware4 disk image
```

So I loaded that up in autopsy and clearly someone was trying to solve the challenge.
Here some interesting snippet found in bash_history (multiple user!)

```bash
ls -la
grep -ri "uoft" .
grep -ri "uoftctf{" .
less .bash_history 
docker ps -a
sudo docker ps -a
sudo docker run -it e3e54039b28b
sudo docker ps -a
sudo docker run -it e3e54039b28b /bin/sh

find ./var/lib/docker/overlay2 -name "*config.txt" 2>/dev/null
find /var/lib/docker/overlay2 -path "*/tmp/*" -type f 2>/dev/null
sudo docker export $(sudo docker create e3e54039b28b) > container.tar
tar -xf container.tar
grep -ri "flag" .
find ./var/lib/docker/overlay2 -name "*config.txt" 2>/dev/null
find /var/lib/docker/overlay2 -path "*/tmp/*" -type f 2>/dev/null
grep -ri "flag" .
grep -ri "uoftctf{" .
grep -ri "flag{" .
env | grep flag
env | grep uoftctf

tar -xf container.tar
grep -ri "flag" .
grep -ri --exclude-dir=bin "flag" .
grep -ri -h="bin" "flag" .
grep -ri -h "bin" "flag" .
find . -type f ! -path "*/bin/*" -print0 | xargs -0 grep -i "flag"
find . -type f ! -path "*/bin/*" -print0 | xargs -0 grep -i "uoftctf"
find . -type f ! -path "*/bin/*" -print0 | xargs -0 grep -i "uoft"

cloud artifacts docker images list   --repository="us-east1-docker.pkg.dev/uoftctf-2025-docker-chal/containers
countdown
gcloud
gcloud artifacts docker images list   --repository="us-east1-docker.pkg.dev/uoftctf-2025-docker-chal/containers
cat flag
cat flag.txt
flag
q
gcloud artifacts docker images list \
  --repository="us-east1-docker.pkg.dev/uoftctf-2025-docker-chal/containers
gcloud artifacts docker images list   --repository="us-east1-docker.pkg.dev/uoftctf-2025-docker-chal/containers
1
2
3
4
5
6
7
8
9
0
1
qqqqq
wqerqweqweqwewqeqweqwewqe
kalgkwmlgkwamlgk
-
+
.
"
```