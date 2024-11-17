from pwn import u8, u16, u32, context

context.signed = True
context.endianness = "big"


class DataInputStream:
    def __init__(self, buffer):
        self.bytes = buffer
        self.position = 0

    def is_empty(self):
        return self.position >= len(self.bytes)

    def read(self, length: int):
        result = self.bytes[self.position : self.position + length]
        self.position += length
        return result

    def read_byte(self, **kwargs):
        return u8(self.read(1))

    def read_short(self, **kwargs):
        return u16(self.read(2), **kwargs)

    def read_int(self, **kwargs):
        return u32(self.read(4), **kwargs)
