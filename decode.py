import base64
import zlib

from Crypto.Hash import SHA384
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from decode_number import decode_number
from byte_stream_parser import ByteStreamParser
from renderer import render_uncompressed

PUBLIC_KEY = "AwEAA0VDQ1UAAAABAAwxLjMuMTMyLjAuMzQAYwRhBI1vbBVnA1KE/T1UpdQYzG6LLot++cuCP5DdEdeKtedw5G8RKAhU0KbNXVUwym8CSwUyzdAPC98DAgvkJGOZA/x+cnJOWhVvYTqJvy+IlcOgjSe9kqs0O7zEBy26UmvlIw=="
EXPECTED_CURVE_PARAMS = "1.3.132.0.34"
SOME_EC_POINT = "04AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB73617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F"
ANOTHER_CRYPTO_PARAM = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973"

public_key = base64.b64decode(PUBLIC_KEY)
public_key_preamble, public_key_point = public_key[:28], public_key[30:]

# FIXME: i think we're importing/constructing the key incorrectly
# pk = ECC.import_key(public_key_point, curve_name="NIST P-384")
pk = ECC.construct(
    curve="NIST P-384",
    point_x=21768876250334385725747672907467582086806720528308407299377393892072621925580424420270966419451131233829776989815371,
    point_y=800115138542352385268888331835970223045897418344421089670732162051188097710073126270498232678219200858362384999715,
)
print(pk)

# FIXME: not sure which one it's supposed to be
randfunc = "deterministic-rfc6979"
# rand_func = "fips-186-3"

verifier = DSS.new(pk, randfunc, encoding="binary")

# print(base64.b64decode(PUBLIC_KEY))
# print(base64.b64decode(PUBLIC_KEY)[30:].hex())

number = ""
with open("data.dat") as f:  # QR code scan result
    number = f.read().strip()

data = decode_number(number)
print(data.hex())
print()

parsed_bytestream = ByteStreamParser(data)

expected_signature = (
    bytes.fromhex("30640230")  # TODO: extract these from `data`
    + parsed_bytestream.a[:48]
    + bytes.fromhex("0230")  # TODO: extract these from `data`
    + parsed_bytestream.a[48:]
)
print()
print(expected_signature.hex())

hashed = SHA384.new(parsed_bytestream.b)
print()
print(hashed.digest().hex())
print()

try:
    verifier.verify(hashed, expected_signature)
    print("verification passed")
except Exception:
    print("verification failed")

pic = data[15:1199]  # TODO: un-hardcode and decode (if it exists)
print()
print(pic.hex())
print()

compressed_fields = parsed_bytestream.zip_payloads[0][2:]
print("compressed data", compressed_fields.hex())

decompressed_fields = zlib.decompress(compressed_fields)
print(decompressed_fields.hex())
print()

render_uncompressed(decompressed_fields)
