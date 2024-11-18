import zlib
import logging

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

from .decode_number import decode_number
from .byte_stream_parser import ByteStreamParser
from .crypto import CURVE, PUBLIC_KEY_POINT, HASH
from .renderer import render_uncompressed

logger = logging.getLogger(__name__)


def decode_pan_code(number: str) -> str:
    data = decode_number(number)
    logger.debug("decoded bytestream: %s", data.hex())

    parsed_bytestream = ByteStreamParser(data)
    logger.debug("body: %s", parsed_bytestream.body.hex())

    r = int.from_bytes(parsed_bytestream.signature[:48], byteorder="big")
    s = int.from_bytes(parsed_bytestream.signature[48:], byteorder="big")
    expected_signature = encode_dss_signature(r, s)
    logger.debug("expected signature (der): %s", expected_signature.hex())

    public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        CURVE(),
        PUBLIC_KEY_POINT,
    )

    try:
        public_key.verify(expected_signature, parsed_bytestream.body, ec.ECDSA(HASH()))
        logger.info("verification passed")
    except Exception:
        print("error: verification failed")
        exit(2)

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
