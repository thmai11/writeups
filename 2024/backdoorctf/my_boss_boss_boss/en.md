# My boss's boss's boss

We are given a pdf file.
Inspecting the PDF file we have the following suspicious object

```
999 0 obj
<</Type/Whoop/Subtype/Somezipfile1/WE9SXzU3/Bytes[7 28 84 83 67 87 94 87 95 87 207 42 195 14 239 93 181 65 243 87 87 87 202 87 87 87 92 87 75 87 49 59 54 48 121 35 54 37 121 48 45 2 3 94 87 84 207 20 50 48 207 20 50 48 34 47 92 87 86 83 191 84 87 87 83 191 84 87 87 42]/NM(fitz-A0)>>
endobj

999 0 obj
<</Type/Whoop/Subtype/Somezipfile2/WE9SXzU3/Bytes[107 178 250 164 219 128 205 238 20 73 15 210 123 107 23 71 205 82 247 2 208 43 56 140 97 47 99 60 217 219 42 57 252 177 167 32 34 3 43 213 209 123 132 205 141 27 178 214 170 128 64 175 24 96 21 213 177 143 246 207 15 96 65 236 170 244 89 70 23 39]/NM(fitz-A0)>>
endobj

999 0 obj
<</Type/Whoop/Subtype/Somezipfile3/WE9SXzU3/Bytes[128 4 246 153 196 114 186 181 48 201 224 175 90 187 127 83 174 24 19 118 96 215 172 179 118 146 237 41 49 72 217 131 210 242 112 253 81 71 210 153 239 89 121 198 173 129 124 1 56 51 209 180 39 24 230 189 15 143 123 222 187 25 175 8 191 240 22 32 86 8]/NM(fitz-A0)>>
endobj

999 0 obj
<</Type/Whoop/Subtype/Somezipfile4/WE9SXzU3/Bytes[253 150 241 219 166 211 115 189 88 42 45 152 215 2 112 4 45 190 123 40 219 124 184 7 28 80 95 239 93 181 65 243 87 87 87 202 87 87 87 7 28 86 85 73 84 67 87 94 87 95 87 207 42 195 14 239 93 181 65 243 87 87 87 202 87 87 87 92 87 79]/NM(fitz-A0)>>
endobj

999 0 obj
<</Type/Whoop/Subtype/Somezipfile5/WE9SXzU3/Bytes[87 87 87 87 87 87 87 87 87 227 214 87 87 87 87 49 59 54 48 121 35 54 37 121 48 45 2 3 82 87 84 207 20 50 48 34 47 92 87 86 83 191 84 87 87 83 191 84 87 87 7 28 82 81 87 87 87 87 86 87 86 87 6 87 87 87 174 87 87 87 87 87]/NM(fitz-A0)>>
endobj
```

The signature dosnt match the zip file signature

> I overlooked this but WE9SXzU3 is XOR_57 in base64

I wrote a script to try to get the signature matching.

```python
import binascii

def xor_bytes(data, key):
    return bytes([b ^ key for b in data])

def is_zip_signature(data):
    zip_signature = bytes([0x50, 0x4B, 0x03, 0x04])
    return data[:4] == zip_signature

bytes1 = [7, 28, 84, 83, 67, 87, 94, 87, 95, 87, 207, 42, 195, 14, 239, 93,
          181, 65, 243, 87, 87, 87, 202, 87, 87, 87, 92, 87, 75, 87, 49, 59,
          54, 48, 121, 35, 54, 37, 121, 48, 45, 2, 3, 94, 87, 84, 207, 20,
          50, 48, 207, 20, 50, 48, 34, 47, 92, 87, 86, 83, 191, 84, 87, 87,
          83, 191, 84, 87, 87, 42]

bytes2 = [107, 178, 250, 164, 219, 128, 205, 238, 20, 73, 15, 210, 123, 107, 23, 71,
          205, 82, 247, 2, 208, 43, 56, 140, 97, 47, 99, 60, 217, 219, 42, 57, 252, 177,
          167, 32, 34, 3, 43, 213, 209, 123, 132, 205, 141, 27, 178, 214, 170, 128, 64, 175,
          24, 96, 21, 213, 177, 143, 246, 207, 15, 96, 65, 236, 170, 244, 89, 70, 23, 39]

bytes3 = [128, 4, 246, 153, 196, 114, 186, 181, 48, 201, 224, 175, 90, 187, 127, 83, 174, 24, 
          19, 118, 96, 215, 172, 179, 118, 146, 237, 41, 49, 72, 217, 131, 210, 242, 112, 253, 
          81, 71, 210, 153, 239, 89, 121, 198, 173, 129, 124, 1, 56, 51, 209, 180, 39, 24, 230, 
          189, 15, 143, 123, 222, 187, 25, 175, 8, 191, 240, 22, 32, 86, 8]

bytes4 = [253, 150, 241, 219, 166, 211, 115, 189, 88, 42, 45, 152, 215, 2, 112, 4, 45, 190, 
          123, 40, 219, 124, 184, 7, 28, 80, 95, 239, 93, 181, 65, 243, 87, 87, 87, 202, 87, 
          87, 87, 7, 28, 86, 85, 73, 84, 67, 87, 94, 87, 95, 87, 207, 42, 195, 14, 239, 93, 
          181, 65, 243, 87, 87, 87, 202, 87, 87, 87, 92, 87, 79]

bytes5 = [87, 87, 87, 87, 87, 87, 87, 87, 87, 227, 214, 87, 87, 87, 87, 49, 59, 54, 48, 121, 
          35, 54, 37, 121, 48, 45, 2, 3, 82, 87, 84, 207, 20, 50, 48, 34, 47, 92, 87, 86, 
          83, 191, 84, 87, 87, 83, 191, 84, 87, 87, 7, 28, 82, 81, 87, 87, 87, 87, 86, 87, 
          86, 87, 6, 87, 87, 87, 174, 87, 87, 87, 87, 87]

extracted_data = bytes1 + bytes2 + bytes3 + bytes4 + bytes5

for key in range(256):  
    print(f"Testing XOR key: {hex(key)}")
    
    
    xored_data = xor_bytes(extracted_data, key)
    
    
    if is_zip_signature(xored_data):
        print(f"XOR Key {hex(key)} : ZIP detected !")
        with open(f"output_xored_{hex(key)}.bin", "wb") as f:
            f.write(xored_data)
        print(f"Saving file to'output_xored_{hex(key)}.bin'")
        break  
    else:
        print(f"Key XOR {hex(key)} : Failed")
```

This lead to a password protected zip archive.

rockyou.txt did not work.

> Here I lost some time looking at the highlighted data in the pdf which lead to nothing


```
EDIT: It was an unintended solve, In the PDF there was 4 word highlighted: Kayla Banks 68697602 Shelly. We was suposed to build a custom wordlist

But it is in rockyou.txt
cat /usr/share/wordlists/rockyou.txt | grep SHELLY
SHELLY
[...]
```

My teamate searched the `d3ad0ne` reference from the description and its an hashcat rule file 
https://github.com/hashcat/hashcat/blob/master/rules/d3ad0ne.rule

Using this rule file and rockyou.txt

```
$pkzip$1*1*2*0*a4*9d*16e20ab8*0*45*8*a4*7d98*7d3ce5adf38cd79ab9431e58852c3c40109a05a055877c6fdb3678346b8e8c7d6eabe6f07775547c82862cd39ada4ce581fdd717f84f374282e6d8a198583716bbfda30e114070d753a1ce9325ede2679eb7f80dec2804f94f44213780fbe421c5ba7e661f8ed485a527aa061085ceb80e2e91fad62b566f6486e3704fb1ea58d82c89ec4ef85fe8a74177015faac1a68cf18424ea0f7d7acf805527537ae92c7f8c2bef*$/pkzip$:S1H2E3L4L5Y6

Password: S1H2E3L4L5Y6
```

Inside that, another tar.gz which once extracted contained flag.txt:

`flag{ge771ng_y04R_Wh55Ls_t4rn1ng}`
