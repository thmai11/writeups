# My first website

### Information

⚠️ This is a blue-team challenge. There is no flag but a button that will validate that you patched the vulnerability

- webshell
- http://REDACTED


By looking at the `nginx` folder, I found that the authentication process was handle by `.htaccess`


```
admin:$apr1$ylTvWSmW$YKsO3kx3XCS.7OT0ExXFm.
```

I want to be admin so lets use `john` with `rockyou.txt`
```bash
john --show hash.txt 
admin:admin
```

Oh.. erm... not really secured indeed -_-'

```bash
htpasswd .htpasswd admin
```

admin:NEW_SECURE_PASSWORD?

Asking the oracle.... solved!