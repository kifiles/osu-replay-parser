import struct


def parse_uleb128(content):
    tmp = 0
    i = 0
    value = 0
    for i in range(0, 5):
        tmp = content[i] & 0x7f
        value = tmp << (i * 7) | value
        if (content[i] & 0x80) != 0x80:
            break
    if i == 4 and (tmp & 0xf0) != 0:
        print("Invalid ULEB128 number")
        return -1
    return i + 1, value


def unpack(fmt, buf, start, slen):
    return struct.unpack(fmt, buf[start:start + slen])[0]


def parse_string(buf, offset):
    if buf[offset] == 0x00:
        return "", offset + 1
    if buf[offset] != 0x0b:
        raise Exception("Invalid String")

    offset += 1
    ullen, stlen = parse_uleb128(buf[offset:])
    offset += ullen

    return buf[offset:offset + stlen].decode("utf-8"), offset + stlen


def parse_short(buf, offset):
    return struct.unpack("<H", buf[offset:offset + 2])[0], offset + 2


def parse_uint(buf, offset):
    return struct.unpack("<I", buf[offset:offset + 4])[0], offset + 4


def parse_bool(buf, offset):
    return buf[offset] == 1, offset + 1


def parse_long(buf, offset):
    return struct.unpack("<Q", buf[offset:offset + 8])[0], offset + 8


def parse_double(buf, offset):
    return struct.unpack("<d", buf[offset:offset + 8])[0], offset + 8


def winticks_to_unix(ticks):
    return round(ticks / 10000000) + 62135604124


def get_bit(num, offset):
    return bool((num >> offset) & 0x01)
