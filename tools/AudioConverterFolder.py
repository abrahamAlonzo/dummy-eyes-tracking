import os
from pydub import AudioSegment

def getNames(extension,path):
    names = []
    for filename in os.listdir(os.path.join(folderNameInput,'.')):
        if filename.endswith('.' + extension):
            names.append(filename)

    return names


if __name__ == "__main__":
    folderNameInput = 'input'
    folderNameOutput = 'output'
    fromFormat = 'm4a'
    toFormat = 'mp3'
    if not os.path.exists(folderNameOutput):
        os.mkdir(folderNameOutput)

    for track in getNames(fromFormat,folderNameInput):
        song = AudioSegment.from_file(os.path.join(folderNameInput,track))
        song.export(os.path.join(folderNameOutput,track.replace(fromFormat,toFormat)), format=toFormat)

    