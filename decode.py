import base64
import zlib

from Crypto.Hash import SHA384
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

PUBLIC_KEY = "AwEAA0VDQ1UAAAABAAwxLjMuMTMyLjAuMzQAYwRhBI1vbBVnA1KE/T1UpdQYzG6LLot++cuCP5DdEdeKtedw5G8RKAhU0KbNXVUwym8CSwUyzdAPC98DAgvkJGOZA/x+cnJOWhVvYTqJvy+IlcOgjSe9kqs0O7zEBy26UmvlIw=="
EXPECTED_CURVE_PARAMS = "1.3.132.0.34"
SOME_EC_POINT = "04AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB73617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F"
ANOTHER_CRYPTO_PARAM = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973"

public_key = base64.b64decode(PUBLIC_KEY)
public_key_preamble, public_key_point = public_key[:28], public_key[30:]

pk = ECC.import_key(public_key_point, curve_name="NIST P-384")
print(pk)

verifier = DSS.new(pk, "deterministic-rfc6979", encoding="der")
# verifier = DSS.new(pk, "fips-186-3", encoding="der")

# print(base64.b64decode(PUBLIC_KEY))
# print(base64.b64decode(PUBLIC_KEY)[30:].hex())

data = b""
with open("data.hex") as f:
    data = bytes.fromhex(f.readline())

expected_signature = b""
with open("expected-signature.hex") as f:
    expected_signature = bytes.fromhex(f.readline())

hashed = SHA384.new(data[:1361])

try:
    verifier.verify(hashed, expected_signature)
    print("verification passed")
except Exception:
    print("verification failed")

pic = data[15:1199]
der_encoded_signature = data[1361:]
compressed_fields = data[1263:-104]

decompressed_fields = zlib.decompress(compressed_fields)
print(decompressed_fields)
