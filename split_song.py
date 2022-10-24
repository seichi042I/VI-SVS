import music21 as m21
import subprocess
import sys
import os
args = sys.argv


file = m21.converter.parse(args[1])
components = m21.stream.Stream()
for element in file.recurse():
    components.append(element)

file_name=args[1].replace('.musicxml','').split('/')[2]

notes_out=args[1].replace('.musicxml','_phrase.nts')
phrase_phoneme_out=args[1].replace('.musicxml','_phrase.phn')
lab_file=args[1].replace('.musicxml','.lab')
wav_file = args[1].replace('.musicxml','.wav')
print('\n'+notes_out)

note2oct_map={
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
#extract notes and notes duration
with open(notes_out,'w') as n_of:
    sec_par_quart=None
    lyric_list=[]
    notes_list=[]
    dur_list=[]
    tie_list=[]
    phrase_lyric_list=[]
    phrase_notes_list=[]
    phrase_dur_list=[]
    phrase_tie_list=[]
    
    rest_flag = True
    for e in components:
        tie=None
        if e.__class__.__name__ == 'MetronomeMark':
            print('tempo = '+str(e.number))
            print('note/beat = '+str(e.referent.quarterLength))
            sec_par_quart=60.0/e.number/e.referent.quarterLength
            print('second/quarter = '+str(sec_par_quart))
        elif e.__class__.__name__ == 'Note':
            rest_flag = False
            tie=e.tie
            name=e.name
            octave=int(e.octave*12+(note2oct_map[name[0]]))

            octave += name.count('#')
            octave -= name.count('-')
            note = oct2note_map[str(octave%12)]
            octave = str(octave//12)
            if len(note) >= 2:
                note = note[0]+octave+'/'+note[1]+octave
            else:
                note = note[0]+octave
            lyric = e.lyric
            if lyric is None:
                lyric = '・'
            lyric_list.append(lyric)
            notes_list.append(note)
            dur_list.append(str(e.quarterLength*sec_par_quart)) if sec_par_quart is not None else print('sec_par_quart is None')
            tie_list.append('1') if tie is not None else tie_list.append('0')

        elif e.__class__.__name__ == 'Rest':
            if not rest_flag and len(notes_list)>0:
                phrase_lyric_list.append(' '.join(lyric_list))
                phrase_notes_list.append(' '.join(notes_list))
                phrase_dur_list.append(' '.join(dur_list))
                phrase_tie_list.append(' '.join(tie_list))
            lyric_list=[]
            notes_list=[]
            dur_list=[]
            tie_list=[]
            rest_flag = True
    notes_dur_tie = [l+'\n'+p+'\n'+d+'\n'+t for l,p,d,t in zip(phrase_lyric_list,phrase_notes_list,phrase_dur_list,phrase_tie_list)]
    n_of.write('\n'.join(notes_dur_tie))
        

phrase_phoneme_list=[]
phrase_phoneme=[]
phrase_durs=[]
phrase_durs_list=[]
phrase_duration_max=0
phrase_duration=0
begin_time = None
if not os.path.exists('../wav_16k_phrase'):
    os.mkdir('../wav_16k_phrase')

with open(phrase_phoneme_out,'w') as ph_of:
    with open(lab_file,'r') as lab:
        num=0
        for line in lab.readlines():
            b,e,p = line.split(' ')
            p = p.strip()
            if not p == 'pau' and not p == 'sil':
                phrase_phoneme.append(p)

                dur = (float(e) - float(b))*10**-7
                phrase_duration+=dur
                if phrase_duration_max <= dur:
                    phrase_duration_max = dur

                phrase_durs.append(str(dur))

                if begin_time is None:
                    begin_time = float(b)*10**-7

            if p == 'pau' and len(phrase_phoneme)>0:
                phrase_phoneme_list.append(' '.join(phrase_phoneme))
                phrase_durs_list.append(' '.join(phrase_durs))
                
                cmd = 'sox '+wav_file+' -r 16000 -b 16 -c 1 ../wav_16k_phrase/'+file_name+'_'+str(num).zfill(3)+'_bits16.wav'+' trim '+str(begin_time)+' '+str(phrase_duration)
                print(cmd)
                res = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE)
                sys.stdout.buffer.write(res.stdout)
                if phrase_duration_max <= phrase_duration:
                    phrase_duration_max = phrase_duration
                phrase_phoneme=[]
                phrase_durs=[]
                phrase_duration=0
                num += 1
                begin_time=None

    phoneme_dur_pair=[p+'\n'+d for p,d in zip(phrase_phoneme_list,phrase_durs_list)]
    ph_of.write('\n'.join(phoneme_dur_pair))
    print('phrase duration max = ',phrase_duration_max)

