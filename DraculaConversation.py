from PlayAudio import playsound
from random import randint

alphabet = {
    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 'P',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z':'Z',
    1: '1',
    2: '2',
    
}

def CharacterAudio(character):
    playsound('alphabet/' + alphabet[character] + '.mp3' )
      
def InitialDialog():
    playsound('dialogs/InitialBarcodeDialog.mp3')

def LeaveDialog():
    playsound('alphabet/LeaveDialog.mp3')

def ContinueMovingDialog():
    playsound('dialogs/SigueTuCamino.mp3')
    

def StareOneDialog():
    randomConversationNumber = randint(0,2) 
    if 0 == randomConversationNumber:
        playsound('dialogs/SigueTuCamino2.mp3')
    elif 1 == randomConversationNumber:
        playsound('dialogs/SigueTuCamino3.mp3')
    elif 2 == randomConversationNumber:
        playsound('dialogs/SigueTuCamino4.mp3')


def StareTwoDialog():
    playsound('dialogs/PareceQueHoyCenoDoble.mp3')

if __name__ == '__main__':
    CharacterAudio('a')

