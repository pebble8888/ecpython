#!/usr/bin/env ruby

require 'ecdsa'
require 'securerandom'
require 'digest'

def bin_to_hex(s)
  s.each_byte.map { |b| b.to_s(16) }.join
end

group = ECDSA::Group::Secp256k1
n = group.order
p "group order:#{n}"

#sk = 1 + SecureRandom.random_number(n-1)
sk = 3
pk = group.generator.multiply_by_scalar(sk)

p "sk:"
p sk
p "pk:"
p pk

# sign
msg = "0000"
msg_digest = Digest::SHA256::digest(msg)
#nonce = 1 + SecureRandom.random_number(n-1)
nonce = 2
sig = ECDSA.sign(group,sk,msg_digest,nonce)

p "msg_digest:#{msg_digest}"
p "nonce:#{nonce}"
p "sig.r:#{sig.r},#{sig.r.to_s(16)}"
p "sig.s:#{sig.s},#{sig.s.to_s(16)}"

sig_der = ECDSA::Format::SignatureDerString.encode(sig)

p "sig_der:#{sig_der}"
p "sig_def(hex):#{bin_to_hex(sig_der)}"

# verify
v_digest = OpenSSL::Digest::SHA256.digest(msg)
v_sig = ECDSA::Format::SignatureDerString.decode(sig_der)
result = ECDSA.valid_signature?(pk, v_digest, sig)
p "result:#{result}"
