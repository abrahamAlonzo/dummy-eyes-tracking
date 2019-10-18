from pydub import AudioSegment
from pydub.playback import play

if __name__ == "__main__":
    #song = AudioSegment.from_file("alphabet\\A.m4a")
    #song.export("out.mp3", format="mp3")
    song = AudioSegment.from_file("out.mp3")
    play(song)

    