from pydub import AudioSegment
from pydub.playback import play

def playsound(filePath): 
    song = AudioSegment.from_file(filePath)
    play(song)


if __name__ == "__main__":
    #song = AudioSegment.from_file("alphabet\\A.m4a")
    #song.export("out.mp3", format="mp3")
    song = AudioSegment.from_file("dialogs\\LeaveDialog.mp3")
    play(song)
else:
    print("play audio as library")

    
