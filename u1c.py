class U1C:
    """
    I don't even know. Used as part of the byte stream parser. Indirectly determines
    whether the length of a struct is read as a byte or as a short.
    """

    def __init__(self, buffer):
        self.buffer = buffer
        self.position = 0
        self._a = 0
        self.b = 0
        p1 = 0

        while True:
            if p1 >= 5:
                break

            if self.position >= len(self.buffer):
                return

            v0 = self.buffer[self.position]
            self.position += 1

            v1 = self._a
            v3 = v0
            v0 = p1 * 8
            v3 <<= v0
            v0 = v1 | v3
            self._a = v0

            v0 = self.b
            v0 += 8
            self.b = v0

            p1 += 1

    def a(self):
        self.position = 0
        v0 = self.b

        v1 = -1
        v2 = 0x20

        if v0 != v2:
            if v0 == 0:
                return v1
        else:
            if self.position < len(self.buffer):
                v0 = self.buffer[self.position]
                self.position += 1

                if v0 != v1:
                    v3 = self._a
                    v0 <<= v2
                    v0 |= v3
                    self._a = v0
                    self.b = 0x28

        v0 = self._a
        v2 = v0
        v3 = 1

        v2 &= v3
        v0 >>= v3
        self._a = v0
        v0 = self.b
        v0 -= v3
        self.b = v0

        return v2

    def f(self, n: int):
        if n < 1 or n > 0x20:
            raise Exception(f"argument out of range: {n}")

        v0 = self.b
        if v0 == 0:
            raise Exception("eof?")

        v0 = 0
        v1 = 0

        while True:
            if v0 >= n:
                return v1

            v2 = self.a()
            v3 = -1
            if v2 == v3:
                return v1

            v2 <<= v0
            v1 |= v2
            v0 = v0 + 1

        return v1
