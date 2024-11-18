from struct import unpack


class DataInputStream:
    buffer: bytes
    position: int

    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.position = 0

    def is_empty(self) -> bool:
        return self.position >= len(self.buffer)

    def read(self, length: int) -> bytes:
        result = self.buffer[self.position : self.position + length]
        self.position += length
        return result

    def read_byte(self, **kwargs):
        signed = kwargs.get("signed", True)
        fmt = "b" if signed else "B"
        [val] = unpack(fmt, self.read(1))

        return val

    def read_short(self, **kwargs):
        signed = kwargs.get("signed", True)
        fmt = "h" if signed else "H"
        [val] = unpack(">" + fmt, self.read(2))

        return val

    def read_int(self, **kwargs):
        signed = kwargs.get("signed", True)
        fmt = "i" if signed else "I"
        [val] = unpack(">" + fmt, self.read(4))

        return val
