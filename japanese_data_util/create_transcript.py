from re import S
import sys
import os


"""
このリポジトリのVISinger実装で扱うデータフォーマット
ディレクトリ構造
.
├── VISinger
│   ├── prepare
│   │   ├── data_vits.py
│   │   └── ...
│   ├── ...
│   └── train.py
└── VISinber_data
    ├── wav_dump_16k
    └── trainscriptions.txt

wav_dump_16kディレクトリに分割・リサンプリング済みの音声ファイルをすべて入れる

transcriptions.txtのフォーマット
それぞれの要素が「|」でつながれた一行で一つのデータを表す．要素内の区切りはスペース．
音声ファイルごとにこれを改行で区切ってならべたものがtranscriptions.txtになる。

- 音声ファイル名(拡張子なし)
- 歌詞
- 音素
- 音階
- 音階継続長(秒)
- 音素継続長(秒)
- スラー記号がついているか否か(0 or 1)

例
いろは歌01|い ろ は|i r o h a|C3 C3 C3|0.5 0.5 0.5|0.5 0.1 0.4 0.1 0.4|0 0 0
いろは歌02|に ほ へ|n i o e|C3 C3 C3|0.5 0.5 0.5|0.1 0.4 0.5 0.5|0 0 0
"""

args = sys.argv

_, dirs, _ = next(os.walk('.'))

transcriptions = []
for d in dirs:
    file=d+'/'+d
    transcript=[]
    #lyrics
    with open(file+'.ly','r') as f:
        transcript.append(f.readline())

    #phoneme and phoneme durations
    phoneme_list=[]
    phoneme_duration_list=[]
    with open(file+'_phrase.phn','r') as f:
        for i,line in enumerate(f.readlines()):
            
            if i % 2 == 0:
                phoneme_list.append(line.replace('\n','').replace('GlottalStop','gts').replace('Edge','edg'))
            else:
                phoneme_duration_list.append(line.replace('\n',''))
    print(phoneme_list)
    
    # lyric, notes, notes_duration, tie
    lyric_list=[]
    notes_list=[]
    notes_duration_list=[]
    tie_list=[]
    with open(file+'_phrase.nts','r') as f:
        
        for i,line in enumerate(f.readlines()):
            n = i%4
            if n == 0:# lyric
                lyric_list.append(line.replace('\n',''))
            elif n == 1:# notes:
                notes_list.append(line.replace('\n',''))
            elif n == 2:# notes_duration
                notes_duration_list.append(line.replace('\n',''))
            elif n == 3:# tie
                tie_list.append(line.replace('\n',''))
        
    zip_ = zip(
        lyric_list,
        phoneme_list,
        notes_list,
        notes_duration_list,
        phoneme_duration_list,
        tie_list,
        )
    transcript=['|'.join([l,p,n,nd,pd,t]) for l,p,n,nd,pd,t in zip_]

    for i,t in enumerate(transcript):
        transcriptions.append(d+'_'+str(i).zfill(3)+'|'+t)
    
with open('transcriptions.txt','w') as f:
    f.write('\n'.join(transcriptions))
    