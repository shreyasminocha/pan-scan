import logging
from typing import List

from data_input_stream import DataInputStream
from u1c import U1C

logger = logging.getLogger(__name__)


class ByteStreamParser:
    c: int
    d: int
    e: int

    body: bytes
    "non-signature-related bytes"

    signature: bytes

    aux_payloads: List[bytes]
    zip_payloads: List[bytes]

    def __init__(self, buffer: bytes):
        stream = DataInputStream(buffer)

        logger.debug(stream.read_byte())  # this can be 0x6 or 0x3
        logger.debug(stream.read_byte())  # ignored?

        # later checked (in PanHtmlApi via w1/b->b) to determine if there's an error
        self.c = stream.read_int()  # is put into s1/b;->c
        logger.debug(self.c)

        self.d = stream.read_byte()  # is put into s1/b;->d
        logger.debug(self.d)

        self.e = stream.read_short()  # is put into s1/b;->e
        logger.debug(self.e)

        self.aux_payloads = []
        self.zip_payloads = []

        # number of structures to read
        # excluding (1) zipped data, and (2) signature
        num_structs = stream.read_byte()
        logger.debug(num_structs)

        for _ in range(num_structs):
            singleton_buf = [stream.read_byte()]
            logger.debug(singleton_buf[0])

            v11 = U1C(singleton_buf)
            v11.f(3)

            v13 = 1 if v11.a() == 0 else 0
            v11.f(4)  # ??

            if v13 != 1:
                n = stream.read_short(signed=False)
            else:
                n = stream.read_byte()

            logger.debug(n)

            stuffs = stream.read(n)
            self.aux_payloads.append(stuffs)
            logger.debug(stuffs.hex())

        num_zipped_structs = stream.read_byte(signed=False)
        logger.debug(num_zipped_structs)

        for _ in range(num_zipped_structs):
            singleton_buf = [stream.read_byte()]
            logger.debug(singleton_buf[0])

            v11 = U1C(singleton_buf)
            v11.f(3)

            v13 = 1 if v11.a() == 0 else 0
            v11.f(4)

            if v13 != 1:
                n = stream.read_short(signed=False)
            else:
                n = stream.read_byte()

            logger.debug(n)

            stuffs = stream.read(n)
            self.zip_payloads.append(stuffs)
            logger.debug(stuffs.hex())

        self.body = buffer[: stream.position]

        logger.debug(stream.read_byte())  # ??
        logger.debug(stream.read_byte())  # ??
        logger.debug(stream.read_short())  # ??

        n = stream.read_short(signed=False)
        logger.debug(n)

        self.signature = stream.read(n)
        logger.debug(self.signature.hex())

        assert stream.position + 2 == len(buffer)
