import argparse
import json

import util


def parse_lifebar(lb: str):
    newlist = list()
    splitted = lb[:-1].split(",")
    for i in splitted:
        vals = i.split("|")
        newlist.append((int(vals[0]), float(vals[1])))
    return newlist


def parse_standard(rdata: bytes):
    offset = 0

    s300, offset = util.parse_short(rdata, offset)
    s100, offset = util.parse_short(rdata, offset)
    s50, offset = util.parse_short(rdata, offset)
    geki, offset = util.parse_short(rdata, offset)
    katu, offset = util.parse_short(rdata, offset)
    miss, offset = util.parse_short(rdata, offset)
    return {
        "300": s300,
        "100": s100,
        "50": s50,
        "geki": geki,
        "katu": katu,
        "miss": miss
    }


def parse_mods(mods: int):
    return {
        "NoFail": util.get_bit(mods, 0),
        "Easy": util.get_bit(mods, 1),
        "TouchDevice": util.get_bit(mods, 2),
        "Hidden": util.get_bit(mods, 3),
        "HardRock": util.get_bit(mods, 4),
        "SuddenDeath": util.get_bit(mods, 5),
        "DoubleTime": util.get_bit(mods, 6),
        "Relax": util.get_bit(mods, 7),
        "HalfTime": util.get_bit(mods, 8),
        "Nightcore": util.get_bit(mods, 9),
        "Flashlight": util.get_bit(mods, 10),
        "Autoplay": util.get_bit(mods, 11),
        "SpunOut": util.get_bit(mods, 12),
        "Relax2": util.get_bit(mods, 13),
        "Perfect": util.get_bit(mods, 14),
        "Key4": util.get_bit(mods, 15),
        "Key5": util.get_bit(mods, 16),
        "Key6": util.get_bit(mods, 17),
        "Key7": util.get_bit(mods, 18),
        "Key8": util.get_bit(mods, 19),
        "FadeIn": util.get_bit(mods, 20),
        "Random": util.get_bit(mods, 21),
        "LastMod": util.get_bit(mods, 22),
        "TargetPractice": util.get_bit(mods, 23),
        "Key9": util.get_bit(mods, 24),
        "Coop": util.get_bit(mods, 25),
        "Key1": util.get_bit(mods, 26),
        "Key2": util.get_bit(mods, 27),
        "Key3": util.get_bit(mods, 28)
    }


def parse(osr: bytes):
    offset = 0

    mode = osr[0]
    offset += 1

    gamever, offset = util.parse_uint(osr, offset)
    beatmaphash, offset = util.parse_string(osr, offset)
    playername, offset = util.parse_string(osr, offset)
    replayhash, offset = util.parse_string(osr, offset)

    permodeoff = offset
    offset += 12

    totalscore, offset = util.parse_uint(osr, offset)
    maxcombo, offset = util.parse_short(osr, offset)
    perfect, offset = util.parse_bool(osr, offset)
    modsint, offset = util.parse_uint(osr, offset)
    lifebar, offset = util.parse_string(osr, offset)
    timestamp, offset = util.parse_long(osr, offset)

    # datalength, offset = util.parse_uint(osr, offset)
    # offset += datalength
    #
    # scoreid, offset = util.parse_long(osr, offset)
    # modinfo, offset = util.parse_double(osr, offset)

    info = {
        "mode": mode,
        "gamever": gamever,
        "beatmaphash": beatmaphash,
        "playername": playername,
        "replayhash": replayhash,
        "totalscore": totalscore,
        "maxcombo": maxcombo,
        "perfect": perfect,
        "mods": parse_mods(modsint),
        "lifebar": parse_lifebar(lifebar),
        "timestamp": util.winticks_to_unix(timestamp),
        # "scoreid": str(scoreid),
        # "modinfo": modinfo
    }

    permode = {}
    if mode == 0:
        # osu! Standard
        permode = parse_standard(osr[permodeoff:permodeoff + 12])

    info["score"] = permode
    return info


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--input", required=True)
    argparser.add_argument("-o", "--output-file", dest="output")
    args = argparser.parse_args()

    with open(args.input, "rb") as file:
        result = parse(file.read(1024 * 10))
        if args.output is None:
            print(json.dumps(result))
        else:
            with open(args.output, "w") as out:
                out.write(json.dumps(result))
