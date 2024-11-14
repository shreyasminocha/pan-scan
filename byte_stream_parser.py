from enum import Enum

from data_input_stream import DataInputStream


class SCFieldType(Enum):
    SCTextH1 = 0
    SCTextH2 = 1
    SCTextCaption = 2
    SCT = 3
    SCTable = 4
    SCBlob = 5
    SCPlaceHolder = 6
    SCIdentifier = 7
    SCAlign = 8
    SCNewLine = 9
    SCBackground = 10
    SCLIne = 11
    SCHyperLink = 12


class ByteStreamParser:
    def __init__(self, buffer):
        stream = DataInputStream(buffer)

        print(stream.read_byte())  # this can be 0x6 or 0x6
        print(stream.read_byte())  # ignored?
        self.c = stream.read_int()  # is put into s1/b;->c
        print(self.c)
        self.d = stream.read_byte()  # is put into s1/b;->d
        print(self.d)

        self.e = stream.read_short()  # is put into s1/b;->e
        print(self.e)
        # and'd with 0xff and compared with 0x0 (verifying nonnegative?)
        print(stream.read_byte())
        # set as the first and only element of s1/b;->g:Ljava/util/ArrayList
        self.g = [stream.read_byte()]
        print(self.g[0])

        n = stream.read_short(signed=False)
        print(n)

        stuffs = stream.read(n)
        print(stuffs.hex())

        print(stream.read_byte())
        n = stream.read_byte()
        print(n)

        stuffs = stream.read(n)
        print(stuffs.hex())

        print(stream.read_byte())
        print(stream.read_byte())
        n = stream.read_byte()
        print(n)

        stuffs = stream.read(n)
        print(stuffs.hex())

        self.b = buffer[: stream.position]

        print(stream.read_byte())
        print(stream.read_byte())
        print(stream.read_short())
        n = stream.read_short(signed=False)
        print(n)

        self.a = stream.read(n)
        print(self.a.hex())

        assert stream.position + 2 == len(buffer)
