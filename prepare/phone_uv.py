<<<<<<< HEAD:VISinger/prepare/phone_uv.py
# 普通话发音基础声母韵母
# 普通话声母只有 4 个浊音：m、n、l、r，其余 17 个辅音声母都是清音
# 汉语拼音的 y 和 w 只出现在零声母音节的开头，它们的作用主要是使音节界限清楚。
# https://baijiahao.baidu.com/s?id=1655739561730224990&wfr=spider&for=pc

uv_map = {
    "u":1,
    "o":1,
    "i":1,
    "e":1,
    "a":1,
    "U":0,
    "O":0,
    "N":1,
    "I":0,
    "E":0,
    "A":0,
    "b":0,
    "by":0,
    "ch":0,
    "cl":0,
    "gts":0,
    "edg":0,
    "d":0,
    "dy":0,
    "f":0,
    "fy":0,
    "g":0,
    "gy":0,
    "h":0,
    "hy":0,
    "j":0,
    "k":0,
    "ky":0,
    "m":0,
    "my":0,
    "n":0,
    "ny":0,
    "p":0,
    "py":0,
    "r":0,
    "ry":0,
    "s":0,
    "sh":0,
    "sl":0,
    "t":0,
    "ts":0,
    "ty":0,
    "v":0,
    "vy":0,
    "w":0,
    "y":0,
    "z":0,
    "<blank>":0,
    "<sos/eos>":0,
    "br":0,
    "pau":0,
    "<unk>":0,
    "sil":0
=======
# 普通话发音基础声母韵母
# 普通话声母只有 4 个浊音：m、n、l、r，其余 17 个辅音声母都是清音
# 汉语拼音的 y 和 w 只出现在零声母音节的开头，它们的作用主要是使音节界限清楚。
# https://baijiahao.baidu.com/s?id=1655739561730224990&wfr=spider&for=pc

uv_map = {
    "unk":0,
    "sos":0,
    "eos":0,
    "ap":0,
    "sp":0,
    "b":0,
    "c":0,
    "ch":0,
    "d":0,
    "f":0,
    "g":0,
    "h":0,
    "j":0,
    "k":0,
    "l":1,
    "m":1,
    "n":1,
    "p":0,
    "q":0,
    "r":1,
    "s":0,
    "sh":0,
    "t":0,
    "w":1,
    "x":0,
    "y":1,
    "z":0,
    "zh":0,
    "a":1,
    "ai":1,
    "an":1,
    "ang":1,
    "ao":1,
    "e":1,
    "ei":1,
    "en":1,
    "eng":1,
    "er":1,
    "i":1,
    "ia":1,
    "ian":1,
    "iang":1,
    "iao":1,
    "ie":1,
    "in":1,
    "ing":1,
    "iong":1,
    "iu":1,
    "o":1,
    "ong":1,
    "ou":1,
    "u":1,
    "ua":1,
    "uai":1,
    "uan":1,
    "uang":1,
    "ui":1,
    "un":1,
    "uo":1,
    "v":1,
    "van":1,
    "ve":1,
    "vn":1
>>>>>>> 86c21c0f0eaf39f3cef8ea34f0e681d7f38751a1:prepare/phone_uv.py
}