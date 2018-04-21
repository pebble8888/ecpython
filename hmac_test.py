import hmac
import hashlib

sk = str("secret").encode('utf-8')
msg = str("message").encode('utf-8')
sig = hmac.new(sk, msg, hashlib.sha512).hexdigest()
print(sig)
print(len(sig))
