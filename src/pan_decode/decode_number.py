from itertools import batched
from typing import List


class DecodeNumber:  # u1b
    """
    Class that converts the QR code scan result into the bytestream that the rest of the
    code processes.

    Painstakingly reimplemented from the disassembly of the class "u1.b", especially the
    "a(II)V" method.
    """

    _a: int
    _b: int
    buf: List[int]

    def __init__(self):
        self._a = 0
        self._b = 0
        self.buf = []

    def a(self, a: int, b: int):
        if b > 0x20 or b < 0x1:
            raise Exception("out of range")  # i forgor the range

        v0 = self._b

        v1 = v0 + b
        v2 = 0x8

        if not (v0 <= 0) or not (v1 < v2):  # before :cond_0
            v1 = self._a
            v3 = a << (v0 & 0x1F)
            v1 |= v3
            v1 = v1 & 0xFF
            self._a = v1

            v3 = 0x8 - v0
            a = a >> (v3 & 0x1F)
            v2 -= v0
            b -= v2

            self.buf.append(v1)

            v0 = 0x0
            self._a = v0
            self._b = v0

        # cond_0:
        while True:
            v0 = b // 0x8
            if v0 <= 0:
                break  # :cond_1

            v0 = a & 0xFF
            self.buf.append(v0)

            a = a >> (0x8 & 0x1F)
            b = b + (-0x8)

        if b <= 0:  # :cond_1
            return  # :cond_2

        v0 = self._a
        v1 = self._b

        a = a << (v1 & 0x1F)
        a |= v0
        a = a & 0xFF

        self._a = a

        v1 += b
        self._b = v1


def decode_number(number: str) -> bytes:
    u1b_instance = DecodeNumber()
    # this can be something else in some circumstances
    # maybe if instead of a "singlecode" it's a "multicode" or something?
    bval = 0xD

    for t in batched(number, 4):
        chunk = "".join(t)
        aval = int(chunk)

        u1b_instance.a(aval, bval)

    v0 = u1b_instance._b
    if not (v0 <= 0):
        v0 = u1b_instance._a
        u1b_instance.buf.append(v0)

    return bytes(u1b_instance.buf)
