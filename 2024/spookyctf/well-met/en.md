# Well-Met

## Description
```
For the past three years these characters have appeared in JerseyCTF, SpringForwardCTF, and SpookyCTF - but their lore was kept secret. Can you find the secret in their history?
```

## Developer: Cyb0rgSw0rd https://github.com/alfredsimpson

I visited the `lore` page https://spookyctf.ctfd.io/lore
I searched up within the source: `NICC{`

Found:
```html
<p class="redacted" id="spookyflag_part1">NICC{StOr</p>
```
I kept browsing the DOM and found:
```html
<img class="img-fluid" src="/files/img/nah4real.png" width="400" height="400" id="spookyflag_p2" alt="IeS_DoNt_M"/>
<!--<p4>oO_cTfY_rIgHt?}</p4> -->
<span class="p-l redacted" id="p3">aKe_ThE_cTf_T</span>
```
It yield 
```
NICC{StOrIeS_DoNt_MaKe_ThE_cTf_ToO_cTfY_rIgHt?}
```