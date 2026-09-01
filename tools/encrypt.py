#!/usr/bin/env python3
"""Encrypt index.src.html into a password-gated index.html for GitHub Pages.
Usage: python3 tools/encrypt.py <password> [src] [out]
The repo only ever holds the encrypted page. Keep index.src.html private."""
import sys, os, base64, secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

pw = sys.argv[1]
src = sys.argv[2] if len(sys.argv)>2 else 'index.src.html'
out = sys.argv[3] if len(sys.argv)>3 else 'index.html'
ITER = 150000
salt = secrets.token_bytes(16)
iv = secrets.token_bytes(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode())
ct = AESGCM(key).encrypt(iv, open(src,'rb').read(), None)
b64 = lambda b: base64.b64encode(b).decode()

loader = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Ribble Outliers · Sponsor Deck 2027</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,700;9..40,900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"DM Sans",Arial,sans-serif;background:#5C1240;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center}
.gate{padding:40px;max-width:480px;width:100%}
.gate img{width:min(360px,80vw);margin:0 auto 30px;display:block}
h1{font-weight:900;font-size:1.5rem;margin-bottom:.4em}
p{color:#FBD9EA;margin-bottom:1.6em;font-size:.98rem}
input{width:100%;padding:15px 18px;border-radius:12px;border:2px solid #B4155C;background:#7A1E52;color:#fff;font-size:1.05rem;font-family:inherit;text-align:center;letter-spacing:.1em;outline:none}
input:focus{border-color:#EC1E79}
button{margin-top:14px;width:100%;padding:15px;border:0;border-radius:999px;background:#EC1E79;color:#fff;font-weight:900;font-size:1rem;font-family:inherit;cursor:pointer;letter-spacing:.06em}
button:hover{background:#fff;color:#EC1E79}
.err{color:#F9A8CE;font-size:.85rem;margin-top:12px;min-height:1.2em}
</style>
</head>
<body>
<div class="gate">
 <img src="img/logo-white.png" alt="Ribble Outliers">
 <h1>Partner preview, 2027</h1>
 <p>This preview is shared privately. Enter the access code from your invitation, or use your personal link.</p>
 <input id="pw" type="password" placeholder="ACCESS CODE" autocomplete="off">
 <button id="go">Open</button>
 <div class="err" id="err"></div>
</div>
<script>
var SALT="__SALT__", IV="__IV__", CT="__CT__", ITER=__ITER__;
function b2a(b){var s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u;}
function tryOpen(pw, remember){
  if(!pw) return;
  var enc=new TextEncoder();
  crypto.subtle.importKey('raw',enc.encode(pw),'PBKDF2',false,['deriveKey']).then(function(km){
    return crypto.subtle.deriveKey({name:'PBKDF2',salt:b2a(SALT),iterations:ITER,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
  }).then(function(key){
    return crypto.subtle.decrypt({name:'AES-GCM',iv:b2a(IV)},key,b2a(CT));
  }).then(function(buf){
    if(remember){ try{localStorage.setItem('ro27k',pw);}catch(e){} }
    var html=new TextDecoder().decode(buf);
    document.open(); document.write(html); document.close();
  }).catch(function(){
    document.getElementById('err').textContent='That code did not work. Check your invitation.';
  });
}
var m=location.hash.match(/k=([^&]+)/);
if(m){ tryOpen(decodeURIComponent(m[1]), true); }
else{ try{ var s=localStorage.getItem('ro27k'); if(s) tryOpen(s,false); }catch(e){} }
document.getElementById('go').addEventListener('click',function(){ tryOpen(document.getElementById('pw').value.trim(), true); });
document.getElementById('pw').addEventListener('keydown',function(e){ if(e.key==='Enter') tryOpen(e.target.value.trim(), true); });
</script>
</body>
</html>"""
html = loader.replace('__SALT__', b64(salt)).replace('__IV__', b64(iv)).replace('__CT__', b64(ct)).replace('__ITER__', str(ITER))
open(out,'w').write(html)
print('encrypted', src, '->', out, len(html)//1024, 'KB')
