from .data_input_stream import DataInputStream
from .u1c import U1C


class ControlByte:
    SEPARATOR = 0x09
    TEMPLATE_IMAGE = 0x48
    TEMPLATE_TEXT_1 = 0x06
    TEMPLATE_TEXT_2 = 0x08
    IMAGE_OR_PLACEHOLDER = 0x07
    FREEFORM_TEXT = 0x02


def render_uncompressed(buffer: bytes) -> str:
    contents = ""

    stream = DataInputStream(buffer)
    count = stream.read_short()

    for _ in range(count):
        v8 = stream.read_byte()

        v9 = [v8]
        u1c = U1C(v9)

        u1c.f(4)
        u1c.f(4)

        while v8 == ControlByte.SEPARATOR and not stream.is_empty():
            v8 = stream.read_byte()

        if stream.is_empty():
            break

        # talign = stream.read_byte()
        type_ = stream.read_byte()

        match type_:
            case ControlByte.TEMPLATE_IMAGE:
                _ = stream.read_byte()
                # TODO

            case [ControlByte.TEMPLATE_TEXT_1, ControlByte.TEMPLATE_TEXT_2]:
                _ = stream.read_byte()
                # TODO

            case ControlByte.IMAGE_OR_PLACEHOLDER:
                contents += "[image/placeholder payload]\n"
                _ = stream.read_byte()
                # TODO

            case ControlByte.FREEFORM_TEXT:
                # TODO: this can also be a short
                length = stream.read_byte(signed=False)
                text = stream.read(length)
                contents += text.decode() + "\n"

    return contents
