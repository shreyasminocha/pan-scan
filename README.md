# PAN Card Decoder

Decodes the heavily obfuscated contents of QR codes on Indian [PAN cards](https://en.wikipedia.org/wiki/Permanent_account_number).

## Installation

```sh
pip install .
```

## Usage

```sh
echo "0259000000000..." > data.dat
pan-decode data.dat
```
