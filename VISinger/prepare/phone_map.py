_pause = ["<blank>", "<sos/eos>", "br", "pau","<unk>","sil"]

_initials = [
    "b",
    "by",
    "ch",
    "cl",
    'gts',
    'edg',
    "d",
    "dy",
    "f",
    "fy",
    "g",
    "gy",
    "h",
    "hy",
    "j",
    "k",
    "ky",
    "m",
    "my",
    "n",
    "ny",
    "p",
    "py",
    "r",
    "ry",
    "s",
    "sh",
    "sl",
    "t",
    "ts",
    "ty",
    "v",
    "vy",
    "w",
    "y",
    "z",
]

_finals = [
    "u",
    "o",
    "i",
    "e",
    "a",
    "U",
    "O",
    "N",
    "I",
    "E",
    "A",
]

symbols = _pause + _initials + _finals

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def label_to_ids(phones):
    # use lower letter
    sequence = [_symbol_to_id[symbol.lower()] for symbol in phones]
    return sequence


def ids_to_label(ids):
    # use lower letter
    sequence = [_id_to_symbol[id] for id in ids]
    return sequence
