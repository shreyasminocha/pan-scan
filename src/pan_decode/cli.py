import sys
import logging
import argparse

from .decode import decode_pan_code


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog="pan-decode",
        description="Decodes Indian PAN cards",
    )

    parser.add_argument(
        "filename",
        help="Path to the QR code data",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )

    args = parser.parse_args()

    number = args.filename.read().strip()
    contents = decode_pan_code(number)

    print(contents)


if __name__ == "__main__":
    main()
