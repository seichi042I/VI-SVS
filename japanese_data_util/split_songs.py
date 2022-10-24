from ast import arg
from typing import *
import music21 as m21
import subprocess
import sys
import os

octave_fraction_map={
        'C':0.0,
        'D':2.0,
        'E':4.0,
        'F':5.0,
        'G':7.0,
        'A':9.0,
        'B':11.0,
        }
oct2note_map={
    '0':['C'],
    '1':['C#','Db'],
    '2':['D'],
    '3':['D#','Eb'],
    '4':['E'],
    '5':['F'],
    '6':['F#','Gb'],
    '7':['G'],
    '8':['G#','Ab'],
    '9':['A'],
    '10':['A#','Bb'],
    '11':['B'],
}

def cmd_find_name(name: str, folder: str) -> List[str]:
    """
    find コマンドのnameオプションでフォルダを検索する
    Args:
        name: 検索文字列
        folder: 検索ディレクトリのパス
    """
    cmd = 'find ' + folder + ' -name "' + name + '" | sort'
    print(cmd)
    res = subprocess.check_output(cmd, shell=True, text=True).split('\n')
    return list(filter(None,res))

def score_extract(file: m21.score.Score, output: str) -> bool:
    """
    musicxmlまたはxmlから必要な情報を抽出
    Args:
        file: m21.converter.parse()で読み込んだもの
        output: 出力ファイルのパス
    """
    
    components = m21.stream.Stream()
    for element in file.recurse():
        components.append(element)

    # 各出力ファイル名
    # output
    
    print('\n'+output)
    
    #extract notes and notes duration
    sec_par_quart=None
    lyric_list=[]
    notes_list=[]
    dur_list=[]
    tie_list=[]
    phrase_lyric_list=[]
    phrase_notes_list=[]
    phrase_dur_list=[]
    phrase_tie_list=[]
    
    rest_flag = True    # ひとつ前のノートが休符かどうか
    for e in components:
        tie=None
        if e.__class__.__name__ == 'MetronomeMark':
            print('tempo = '+str(e.number))
            print('note/beat = '+str(e.referent.quarterLength))
            sec_par_quart=60.0/e.number/e.referent.quarterLength
            print('second/quarter = '+str(sec_par_quart))
        elif e.__class__.__name__ == 'Note':
            rest_flag = False
            tie = e.tie
            name = e.name

            # オクターブの値から，半音を単位とする数値を算出
            octave_fraction = int(
                e.octave*12+
                (octave_fraction_map[name[0]])
                )

            octave_fraction += name.count('#')  # #の数を足す
            octave_fraction -= name.count('-')  # ♭の数を引く

            note = oct2note_map[str(octave_fraction%12)]    # octave_fractionから音階文字列を取得
            octave = str(octave//12)                        # オクターブを取得

            # 黒鍵でなければそのまま，あれば同義の文字列を/で結合
            note = note[0]+octave if len(note) < 2 else note[0]+octave+'/'+note[1]+octave
            
            lyric = e.lyric
            if lyric is None:
                lyric = '・'

            lyric_list.append(lyric)
            notes_list.append(note)
            dur_list.append(str(e.quarterLength*sec_par_quart)) if sec_par_quart is not None else print('sec_par_quart is None')
            tie_list.append('1') if tie is not None else tie_list.append('0')

        elif e.__class__.__name__ == 'Rest':
            # 休符以前が休符でなく，音符リストに音符が入っているならば，フレーズリストに追加
            if not rest_flag and len(notes_list)>0:
                phrase_lyric_list.append(' '.join(lyric_list))
                phrase_notes_list.append(' '.join(notes_list))
                phrase_dur_list.append(' '.join(dur_list))
                phrase_tie_list.append(' '.join(tie_list))

            # 休符で区切るため休符がきたらリストを初期化
            lyric_list=[]
            notes_list=[]
            dur_list=[]
            tie_list=[]
            rest_flag = True
    
    notes_dur_tie = [l+'|'+p+'|'+d+'|'+t for l,p,d,t in zip(phrase_lyric_list,phrase_notes_list,phrase_dur_list,phrase_tie_list)]

    with open(output,"w") as f:
        return f.write('\n'.join(notes_dur_tie))


def lab_extract(lab_file: str, output: str) -> List[List[str]]:
    """
    labファイルから必要な情報を抽出
    Args:
        lab_file: labファイルのパス
        output: 出力ファイルのパス
    """
    phrase_phoneme_list=[]
    phrase_phoneme=[]
    phrase_durs=[]
    phrase_durs_list=[]
    phrase_duration_max=0
    phrase_duration=0
    begin_time = None

    phrase_span_list = []
    
    with open(lab_file,'r') as lab:
        num=0
        for line in lab.readlines():
            b,e,p = line.split(' ')
            p = p.strip()
            if not p == 'pau' and not p == 'sil':
                phrase_phoneme.append(p)
                dur = (float(e) - float(b)) 
                dur *= 10**-7 if dur_unit == "10us" else 1
                phrase_duration+=dur
                if phrase_duration_max <= dur:
                    phrase_duration_max = dur

                phrase_durs.append(str(dur))

                if begin_time is None:
                    begin_time = float(b)
                    if dur_unit == "10us":
                        begin_time = float(b)*10**-7

            if p == 'pau' and len(phrase_phoneme)>0:
                phrase_phoneme_list.append(' '.join(phrase_phoneme))
                phrase_durs_list.append(' '.join(phrase_durs))
                phrase_span_list.append([str(begin_time),str(phrase_duration)])

                if phrase_duration_max <= phrase_duration:
                    phrase_duration_max = phrase_duration
                phrase_phoneme=[]
                phrase_durs=[]
                phrase_duration=0
                num += 1
                begin_time=None

    with open(phn_out,'w') as ph_of:
        phoneme_dur_pair=[p+'\n'+d for p,d in zip(phrase_phoneme_list,phrase_durs_list)]
        ph_of.write('\n'.join(phoneme_dur_pair))
        print('phrase duration max = ',phrase_duration_max)
    
    return phrase_span_list

args = sys.argv

folder = args[1]# 検索場所
out_file_name_header = args[2]# soxで変換した出力音声のファイル名の先頭に付け加える文字列
dur_unit = args[3]# durationの単位


# labファイルのパスリストを取得
lab_file_path_list = cmd_find_name("*.lab",folder)

# 拡張子なしのbasenameリスト
file_name_list =[os.path.basename(x).replace('.lab','') for x in lab_file_path_list]

# .musicxmlまたは.xmlファイルのパスリストを取得
res = cmd_find_name("*.musicxml",folder)
score_file_path_list = res if res else cmd_find_name("*.xml",folder)

assert score_file_path_list, print('.musicxml or .xml files are not exist.')

# wavファイルのパスリストを取得
wav_file_path_list = cmd_find_name("*.wav",folder)

assert wav_file_path_list, print('wav files are not exist.')

# outputディレクトリ作成
output_dir = 'split_songs_output'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# 各曲ループ
for i,file_name in enumerate(file_name_list):
    # scoreファイルを展開
    file = m21.converter.parse(score_file_path_list[i])
    
    # 曲ごとにoutputディレクトリを作成
    song_out_dir = '/'.join([output_dir, file_name])
    if not os.path.exists(song_out_dir):
        os.mkdir(song_out_dir)
    
    # 出力ファイルパスを作成
    nts_out = song_out_dir + '/' + out_file_name_header + file_name + '_phrase.nts'

    score_extract(file, nts_out)

    phn_out = nts_out.replace('.nts','.phn')

    # lab wav ファイルのパス
    lab_file = lab_file_path_list[i]
    wav_file = wav_file_path_list[i]

    phrase_span_list = lab_extract(lab_file, phn_out)




wav_out_dir+out_file_name_header+file_name+'_'+str(num).zfill(3)+'_bits16.wav'
def sox(
        infile: str, 
        outfile: str, 
        g_options: Optional[str],
        f_in_options: Optional[str],
        f_out_options: Optional[str], 
        effect: Optional[str]
    ):
    cmd = ['sox',g_options, f_in_options, infile, f_out_options, outfile, effect]
    print(cmd)

    res = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE)
    return sys.stdout.buffer.write(res.stdout)