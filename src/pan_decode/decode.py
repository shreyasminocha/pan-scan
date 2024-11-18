import zlib
import logging

from Crypto.Hash import SHA384
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from .decode_number import decode_number
from .byte_stream_parser import ByteStreamParser
from .public_key import PUBLIC_KEY_CURVE, PUBLIC_KEY_X, PUBLIC_KEY_Y
from .renderer import render_uncompressed

logger = logging.getLogger(__name__)


def decode_pan_code(number: str) -> str:
    data = decode_number(number)
    logger.debug("decoded bytestream: %s", data.hex())

    parsed_bytestream = ByteStreamParser(data)

    expected_signature = (
        bytes.fromhex("30640230")  # TODO: extract these from `data`
        + parsed_bytestream.signature[:48]
        + bytes.fromhex("0230")  # TODO: extract these from `data`
        + parsed_bytestream.signature[48:]
    )
    logger.debug("expected signature: %s", expected_signature.hex())

    hashed = SHA384.new(parsed_bytestream.body)
    logger.debug("checksum: %s", hashed.digest().hex())

    # public_key = base64.b64decode(PUBLIC_KEY)
    # public_key_preamble, public_key_point = public_key[:28], public_key[30:]

    # FIXME: i think we're importing/constructing the key incorrectly
    # pk = ECC.import_key(public_key_point, curve_name=PUBLIC_KEY_CURVE)
    pk = ECC.construct(
        curve=PUBLIC_KEY_CURVE,
        point_x=PUBLIC_KEY_X,
        point_y=PUBLIC_KEY_Y,
    )
    logger.debug(pk)

    # FIXME: not sure which one it's supposed to be
    mode = "deterministic-rfc6979"
    # mode = "fips-186-3"

    verifier = DSS.new(pk, mode, encoding="binary")

    try:
        verifier.verify(hashed, expected_signature)
        logger.info("verification passed")
    except Exception:
        print("error: verification failed")
        print()

    for payload in parsed_bytestream.aux_payloads:
        # TODO: decode pic (if it exists)
        logger.debug("aux payload: %s", payload.hex())

    assert len(parsed_bytestream.zip_payloads) == 1
    zip_payload = parsed_bytestream.zip_payloads[0]
    compressed_fields = zip_payload[2:]
    logger.debug("compressed data: %s", compressed_fields.hex())

    uncompressed_fields = zlib.decompress(compressed_fields)
    logger.debug("uncompressed data: %s", uncompressed_fields.hex())

    return render_uncompressed(uncompressed_fields)
