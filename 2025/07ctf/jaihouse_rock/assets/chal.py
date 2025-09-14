import sys
import re
import secrets
import os
import subprocess
import tempfile
import base64

FLAG = os.getenv("FLAG")
key = secrets.token_urlsafe(32)

def encrypt_key(key):
    scrambled = [] 
    for i, c in enumerate(key):
        shifted_char = chr((ord(c) + (i + 1)) % 256)
        scrambled.append(shifted_char)
    scrambled_str = ''.join(scrambled)
    result = scrambled_str[::-1]
    return result

def prison_gate():
    gate = '''
     ________
    |        |
    |  ____  |
    |  |  |  |
    |  |  |  |
    |  |__|  |
    |________|
    |   |    |
    |   |    |
    |   |    |
    |   |    |
    |___|____|
    (c) Hard Rock Penitentiary 

    
Enter your decryption function:
Finish your input with $$END$$ on a newline
___________________________________________
    '''
    print(gate)


def print_open_jail():
    print(f"""
          
          YOU DID IT
     _____________________
    |  _________________  |
    | |    _________    | |
    | |   |         |   | |
    | |   |   __    |   | |
    | |   |  |__|   |   | |
    | |   |_________|   | |
    | |                 | |
    | |                 | |
    | |_________________| |
    |_____________________|
${base64.b64decode(FLAG)}
    """)

def jail(code):
    symbol_pattern = r'[^\w\t\n\s,]'
    for line in code:
        symbols = re.findall(symbol_pattern, line)
        if symbols:
            if line.strip() != "$$END$$":
                print(f"How am I supposed to sing that...")
                return False
            
        for char in line:
            if char.isdigit():
                print(f"Where do you think you're at? In a math class? You're a rockstar, be poetic!")
                return False
    return True

def write_down_lyrics(strings, suffix='.rock'):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=suffix) as temp_file:
        for string in strings:
            temp_file.write(string)
        return temp_file

def sing(code):
    code.insert(0,"let something be arguments at 0\n")
    code.extend(["let liberty be decrypt taking something\n","shout liberty\n"])
    encrypted_key = encrypt_key(key)
    file = write_down_lyrics(code)
    try:
        result = subprocess.run(['/rockstar', file.name, encrypted_key], capture_output=True, text=True)
    except Exception as e:
        print(f"Something went really wrong {e}")
        exit(1)
    os.remove(file.name)
    return result.stdout.strip()


def read_until():
    line = ""
    code = []
    while True:
        line = sys.stdin.readline()
        if "$$END$$" in line:
            break
        code.append(line)
    return code

def main():
    prison_gate()
    input_text = read_until()
    valid = jail(input_text)
    if valid:
        if sing(input_text) == key:
            print_open_jail()
        else:
            print("Aw... what happen to your voice..")
    else:
        print("Look on the bright side, you have only 24 years left.")
    exit

if __name__ == "__main__":
    main()