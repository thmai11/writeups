# Stirling:

### Information
- 1 pdf 
- 1 pdf avec mot de passe

Dans le premier PDF j'ai utiliser `qpdf` 

```
qpdf --qdf --object-streams=disable Stirling.pdf decompressed.pdf
```

Je l'ouvre en suite comme du texte:

```
%% Original object ID: 19 0
3 0 obj
<<
  /JS (app.alert\("mdp : Adm!nNDAop"\);)
  /S /JavaScript
>>
endobj
```

Le mot de passe etait `Adm!nNDAop` pour ouvrir le second pdf

![alt text](img/flag.png)