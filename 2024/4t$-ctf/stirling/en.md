# Stirling:

### Information
- 1 pdf 
- 1 pdf password protected

Used `qpdf` for the unprotected PDF

```
qpdf --qdf --object-streams=disable Stirling.pdf decompressed.pdf
```
Opening it as text:
```
%% Original object ID: 19 0
3 0 obj
<<
  /JS (app.alert\("mdp : Adm!nNDAop"\);)
  /S /JavaScript
>>
endobj
```

The password is `Adm!nNDAop` opening the protected PDF.

![alt text](img/flag.png)