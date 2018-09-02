# Intercept


## Problem Statement
>Garry encrypted a message with his public key and mailed it to Monika. Sure Garry is an idiot. The intercepted mail is given below as seen from Monika's side. Decrypt the message to get the key.
[interceptedMail.eml](https://raw.githubusercontent.com/ketankr9/CodefestCTF18/master/writeups/static/interceptedMail_.eml)

## Solution
It can be deduced from the ps that Garry must have also sent his private key along with the email, since Garry used his public key to encrypt the message the only way to decrypt it was with private key of Garry itself, hence he must have also sent his private key too along with the email so that Monika could decrypt it.  
So our first goal is to find the private key in the email.  

First we extract the attachment from interceptedMail_.eml, which includes removing delimiters and decoding bse64 encoded text.
```
$$$\> cat interceptedMail_.eml | head -n2614 | tail -n2578 | tr -d "\n\r" | base64 --decode > attachment.zip
```
Unzip the attachment.  
```
$$$\> unzip attachment.zip
Archive:  attachment.zip
  inflating: flag.enc                
  inflating: Public_Key_Encryption_.docx
```
Since [.docx] files are also unzippable, so basically anything can be hidden in it, which won't even show up if opened directly.
```
$$$\> unzip Public_Key_Encryption_.docx
Archive:  Public_Key_Encryption_.docx
   creating: customXml/
  inflating: customXml/itemProps1.xml  
  inflating: customXml/item1.xml     
   creating: customXml/_rels/
  inflating: customXml/_rels/item1.xml.rels  
   creating: docProps/
  inflating: docProps/core.xml       
  inflating: docProps/app.xml        
   creating: _rels/
  inflating: _rels/.rels             
   creating: word/
  inflating: word/document.xml       
  inflating: word/header1.xml        
  inflating: word/footnotes.xml      
  inflating: word/endnotes.xml       
  inflating: word/settings.xml       
  inflating: word/styles.xml         
  inflating: word/numbering.xml      
  inflating: word/fontTable.xml      
  inflating: word/webSettings.xml    
  inflating: word/stylesWithEffects.xml  
   creating: word/_rels/
  inflating: word/_rels/document.xml.rels  
   creating: word/media/
  inflating: word/media/image2.png   
  inflating: word/media/image3.png   
  inflating: word/media/image1.png   
   creating: word/theme/
  inflating: word/theme/theme1.xml   
  inflating: [Content_Types].xml
```
If you use binwalk to find any private key appended in any image it will give negative result. Since magic bytes of Private Key was modified :(
```
$$$\> binwalk word/media/image1.png

  DECIMAL       HEXADECIMAL     DESCRIPTION
  --------------------------------------------------------------------------------
  0             0x0             PNG image, 603 x 404, 8-bit/color RGBA, non-interlaced
  91            0x5B            Zlib compressed data, compressed
```
If you just print the content of image.jpg you will find a RSA PRIVATE KEY appended to it. Simple copy it to a new file and correct its first line(RSA is missing).
```
$$$\> cat word/media/image1.png
.......[omitted]........
���V�L�
! ���B@d�X�%k����! �U���! �@��*V{�Z! ��B��l��d�!P,D���^! ��("[k0�+��B
                                                                                                      ����yϱ�IEND�B`�-----BEGIN  PRIVATE KEY-----
MIIEpQIBAAKCAQEAwi6zjwdY8hkkQSdzCTp7guXaGVLkH1K+tQrzAELr82mOdlqr
WE0qhrjzliWhCM+jg8ruVmWf1sw2J2YqR6G5gXFF/+f3LEYgAhgZz3yBSLpPcxcO
tI2Lqyyka3Pv8FmvrwbPFP8ZkQxKrz2YC1vYgu9TGLfciq3EOMT7aV7XnU0u+7Vi
HdL1GM2nVtwfxQHIWL+awuxhv9nqd0rBuy9lu5XipJKRXITW4rVD38qKAU/DPSiN
F1RV9iUON3TjMiAi8Z3jtESB7IXoFlpAvpqtrmXjVt+hHPBZAXMUHCB66E3upXz2
JrsucK+s7D1T+8v29C5kUlecGZ37rDvZ30kq+wIDAQABAoIBAQCtFhXFqyX0fsab
MP/QPQn1Ls8OfZ2L8iS9manrFLvfN7rd8ooC5p2+gsPVlWsKQJMfGdcCugkU3Oh0
jBOp0BVbtU1RA0KGe2dylmsDUJao7jF9hBL+i6DwjpVslmZMlpUL7YTO0WjHqu4z
cDLEBTVj2NH4GYODNcrPU35KeVi2A5W/xdErMY41wFVJVUe1XsRztjM4DFxBu4oO
10XCdZIEGfLqSwhlfvDMweNXxIx/dQYSjDyzzTr0LT/elXxLOHT4bQ9d46qQWBew
12dwffijlg3Gr1/0R+s27TvHCbd1w4KNdW+XtH2lY6m515C/4LI8eeworMKyF8JN
y0sbouuZAoGBAOjdmsmws95UMfIlMGFIY9cw5k3Q+rlcRC0Ys9JlLz9V6xaNLHPK
ysg7pP4rqjZJ4q4QVKCBJaOxPo2TSOXnYflc57JXubIi+O+pOmZZsiY5AslcEPwS
geJM7aW5HXYfssWm5habIhE/mayu6TV1PMa8MlBn34lxTHLG8Gx3EQBPAoGBANV5
R3zhEJYQNGUt6IxR5XdRNvoDfPTGto9AxoPf7D5aJpMn2scXXhSdI5kESrqWFVjW
6EmdF/QQIMYH+PMQo6GYPmHMk0I8K72QThSinQ1tTZrTDyhsVjJhsa0R3gISwSc2
BnsmoT76zRwgT+w8qKzb4aiZkEmrQcvVKksYF/OVAoGBAJwjUtFfyQsPOzoYk3r3
VfKJGDMfJ6433oK6aIBvViHKk0nYuPCfDh76VyQR1Rx3qCV8T7IbRkie5Ml680ss
PTY9hCHBzoJSDsZrmvvbsqcMXQD02XKbWjmJyWLwX3+/u1fqE6cet9YG5hyyXy54
AJtkvvvI2krHDDJ9j+G6aEzjAoGAeaxYrLrzYzT1SD40b9Y1/h4SQco/LJ0ebOQ0
wfGdi6SCnBl5P0T4YLN4GL0zgsoMfMhxOZQKlRekNntQz+nJ+k72L3QU8wmsvK1F
c8mDzqVgOEDYQOgO8URxqv2mFnRuF1VZuFO6UFVPFxrrsvCYC36ATkLI1NSB+hYT
tx2SeUkCgYEAyydGPEYC8jfzRhTc5IdmJ181f5e4k1pjrT/NCmIwDR1G6UZDr+qK
udVV2UEL/hUSRE51nu0i1skdktBDkknIiMTyCZWM+05tZCGn93w2EUAm+5ujozdX
j/Y3ilCR0pbf+mgR225qVBXgqwVd0zbwlfLHqFLZpY6XWD5tQ8vUEMY=
-----END RSA PRIVATE KEY-----
```
Decrypt flag.enc with above obtained RSA PRIVATE KEY using openssl.
```
$$$\> cat flag.enc | openssl rsautl -decrypt -inkey ./key.pem
The flag is kristeinStewart_is_5EXY
```
**CodefestCTF{kristeinStewart_is_5EXY}**  
Enjoy.
