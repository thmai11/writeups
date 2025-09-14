flag = "drgn{l3ts_s1gn_4_c0ntr4ct!!}"
key = "ST4RR0CK"

# Encoding function: adds ASCII values of flag and key characters, mod 256
def encode_flag(flag, key):
    encoded = []
    key_length = len(key)
    for i, char in enumerate(flag):
        key_char = key[i % key_length]
        encoded_char = (ord(char) + ord(key_char)) % 256
        encoded.append(encoded_char)
    return encoded

# Encoding the flag
encoded_flag = encode_flag(flag, key)
print(encoded_flag)