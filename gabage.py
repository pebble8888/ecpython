import hmac
import hashlib
from ecdsa import SigningKey, VerifyingKey

priv_file = open("./ecpriv.pem", "r")
priv_key_data = priv_file.read()
priv_file.close()
privkey = SigningKey.from_pem(priv_key_data)

pub_file = open("./ecpub.pem", "r")
pub_key_data = pub_file.read()
pub_file.close()
pubkey = VerifyingKey.from_pem(pub_key_data)

#msg = str("0000").encode('utf-8')
msg = "0000"
#sig = privkey.sign(msg, hashlib.sha512)
sig = privkey.sign(msg)
print("sig len:" + str(len(sig)))
print("sig:" + sig.hex())

result = pubkey.verify(sig, msg, hashlib.sha512) 
print("result: " +str(result))

