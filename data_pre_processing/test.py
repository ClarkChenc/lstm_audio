import os
import music21 as m21

KERN_DATASET_PATH = "./deutschl/test"
ACCEPTABLE_DURATIONS = [
	0.25,
	0.5,
	1.0,
	1.5,
	2, 
	3,
	4
]

def load_songs_in_kern(dataset_path):
    songs = []
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:
            if file[-3:] == "krn":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
                
    return songs

def is_acceptable_song(song, acceptable_duration):
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_duration:
            return False
        
    return True

def transpose(song):
    # get key from song
    parts = song.getElementsByClass(m21.stream.Part)
    mearsure_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = mearsure_part0[0][4]
    
    # using m21 to estimate key
    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")
        
    # get interval for transposition
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))
        
    # reduce all key to C major or A minor to make learning more easy
    transposed_song = song.transpose(interval)
    
    return transposed_song
    

def preprocess(dataset_path):
    print(f"Loading songs...")
    songs = load_songs_in_kern(dataset_path)
    print(f"Loaded {len(songs)} songs")
    
    for song in songs:
        if not is_acceptable_song(song, ACCEPTABLE_DURATIONS):
            continue
        
    pass

songs = load_songs_in_kern(KERN_DATASET_PATH)
print(f"Loaded {len(songs)} songs.")
song = songs[0]
song.show()

transposed_song = transpose(song)
transposed_song.show()
    
    




