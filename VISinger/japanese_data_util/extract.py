import music21 as m21
import sys
args = sys.argv
file = m21.converter.parse(args[1])
components = m21.stream.Stream()
for element in file.recurse():
    components.append(element)

notes_out=args[1].replace('.musicxml','.nts')
notes_dur_out=args[1].replace('.musicxml','.dur')
lyric_out=args[1].replace('.musicxml','.ly')
slur_out=args[1].replace('.musicxml','.slr')
print('\n'+notes_out.replace('.nts',''))

#extract lyrics
lyrics=[]
with open(args[1].replace('.musicxml','.ust'),'r',encoding='shift_jis') as f:
    for l in f.readlines():
        if 'Lyric' in l:
            lyric=l.strip().replace('Lyric=','')
            if lyric != 'R':
                lyrics.append(lyric)
with open(lyric_out,'w') as f:
    f.write(' '.join(lyrics))

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
with open(slur_out,'w') as slr_of:
    with open(notes_dur_out,'w') as nd_of:
        with open(notes_out,'w') as n_of:
            sec_par_quart=None
            notes_list=[]
            dur_list=[]
            tie_list=[]
            for e in components:
                tie=None
                if e.__class__.__name__ == 'MetronomeMark':
                    print('tempo = '+str(e.number))
                    print('note/beat = '+str(e.referent.quarterLength))
                    sec_par_quart=60.0/e.number/e.referent.quarterLength
                    print('second/quarter = '+str(sec_par_quart))
                elif e.__class__.__name__ == 'Note':
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
                    notes_list.append(note)
                    dur_list.append(str(e.quarterLength*sec_par_quart)) if sec_par_quart is not None else print('sec_par_quart is None')
                    tie_list.append('1') if tie is not None else tie_list.append('0')
                elif e.__class__.__name__ == 'Rest':
                    notes_list.append('rest')
                    dur_list.append(str(e.quarterLength*sec_par_quart)) if sec_par_quart is not None else print('sec_par_quart is None')
                    tie_list.append('1') if tie is not None else tie_list.append('0')
            
            n_of.write(' '.join(notes_list))
            nd_of.write(' '.join(dur_list))
            slr_of.write(' '.join(tie_list))