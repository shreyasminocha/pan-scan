from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

CURVE = ec.SECP384R1
HASH = hashes.SHA384
PUBLIC_KEY_POINT = bytes.fromhex(
    "048d6f6c1567035284fd3d54a5d418cc6e8b2e8b7ef9cb823f90dd11d78ab5e770e46f11280854d0a6cd5d5530ca6f024b0532cdd00f0bdf03020be424639903fc7e72724e5a156f613a89bf2f8895c3a08d27bd92ab343bbcc4072dba526be523"
)
