<<<<<<< HEAD:VISinger/prepare/phone_map.py
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
=======
_pause = ["unk", "sos", "eos", "ap", "sp"]

_initials = [
    "b",
    "c",
    "ch",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "sh",
    "t",
    "w",
    "x",
    "y",
    "z",
    "zh",
]

_finals = [
    "a",
    "ai",
    "an",
    "ang",
    "ao",
    "e",
    "ei",
    "en",
    "eng",
    "er",
    "i",
    "ia",
    "ian",
    "iang",
    "iao",
    "ie",
    "in",
    "ing",
    "iong",
    "iu",
    "o",
    "ong",
    "ou",
    "u",
    "ua",
    "uai",
    "uan",
    "uang",
    "ui",
    "un",
    "uo",
    "v",
    "van",
    "ve",
    "vn",
]


symbols = _pause + _initials + _finals

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def label_to_ids(phones):
    # use lower letter
    sequence = [_symbol_to_id[symbol.lower()] for symbol in phones]
    return sequence
>>>>>>> 86c21c0f0eaf39f3cef8ea34f0e681d7f38751a1:prepare/phone_map.py
