# Well-Met

## Description
```
For the past three years these characters have appeared in JerseyCTF, SpringForwardCTF, and SpookyCTF - but their lore was kept secret. Can you find the secret in their history?
```

## Auteur: Cyb0rgSw0rd https://github.com/alfredsimpson

J'ai simplement visiter la page `lore` https://spookyctf.ctfd.io/lore
J'ai fais afficher les sources et rechercher `NICC{`

```html
<p class="redacted" id="spookyflag_part1">NICC{StOr</p>
```
En naviguant dans le DOM
```html
<img class="img-fluid" src="/files/img/nah4real.png" width="400" height="400" id="spookyflag_p2" alt="IeS_DoNt_M"/>
<!--<p4>oO_cTfY_rIgHt?}</p4> -->
<span class="p-l redacted" id="p3">aKe_ThE_cTf_T</span>
```
Les partit sont identifier donc rapidement on arrive a
```
NICC{StOrIeS_DoNt_MaKe_ThE_cTf_ToO_cTfY_rIgHt?}
```