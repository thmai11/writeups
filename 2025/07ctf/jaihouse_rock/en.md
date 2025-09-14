
# JailHouse-Rock
## Misc
## Description
```
After an untold number of tequilas, you found yourself arrested and thrown into jail. But don't fret, I've got a plan — their security is laughable. Unfortunately, you're going to have to help me rock you out of this mess.
nc REDACTED 1337

Author: drgn
```

Flag b64: `MDdDVEZ7cjBjazNkX3kwdTRfdzR5X3QwX2ZyMzNkMG0hISF9` 
Flag `07CTF{r0ck3d_y0u4_w4y_t0_fr33d0m!!!}`

# Solution
The solution to this is to write a rockstar program that pass the validation from the "jail" method.
The program must "decrypt" a random key passed and print it. The server verify if the key is the same as the original. If yes simply print the flag.

Solution are not unique so here is an exemple:
```rockstar
One is a
zero is aaaaaaaaaa 
Min One is aaaaaaaaaa
knock it down
two_fifty_six is aa aaaaa aaaaaa
Reverse takes a string giving Min One times a string

Modulo takes number, diviser
    let quotient be number over diviser
    turn down quotient
    let product be quotient times diviser
    let remainder be number minus product
    if remainder is less than zero
        let result be remainder with diviser 
    otherwise
        let result be remainder 

give back result

decrypt takes crypted
    Key is silence
    let reverses_key be Reverse taking crypted
    let counter be zero
    for key_char in reverses_key
        burn key_char into ascii
        let Offset be counter plus One
        let substracted be ascii minus Offset
        let wrapped be Modulo taking substracted, two_fifty_six
        burn wrapped into new_key
        let key be key with new_key
        build counter up

give back Key

$$END$$
```