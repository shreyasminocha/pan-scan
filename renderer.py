from data_input_stream import DataInputStream
from u1c import U1C


def render_uncompressed(buffer):
    stream = DataInputStream(buffer)
    count = stream.read_short()

    for _ in range(count):
        v8 = stream.read_byte()

        v9 = [v8]
        u1c = U1C(v9)

        v9 = u1c.f(4)
        v9 = u1c.f(4)

        while v8 == 0x09 and not stream.is_empty():
            v8 = stream.read_byte()

        if stream.is_empty():
            break

        # talign = stream.read_byte()
        type_ = stream.read_byte()

        match type_:
            case 0x48:  # template image
                _ = stream.read_byte()
                # TODO

            case [0x06, 0x08]:  # template text
                _ = stream.read_byte()
                # TODO

            case 0x07:
                print("[image/placeholder payload]")
                _ = stream.read_byte()
                # TODO

            case 0x02:  # freeform text
                # TODO: this can also be a short
                length = stream.read_byte(signed=False)
                text = stream.read(length)
                print(text.decode())
