import numpy as np
from scipy.io import wavfile

#example code from site on trello
def speedUP(soundsArray, speedUp):
    indices = np.around(np.arange(0, len(soundsArray), speedUp))
    indices = indices[indices < len(soundsArray)].astype(int)
    return soundsArray[indices.astype(int)]

def trigApply(soundArray, option):
    if(option):
        #np.nditer defines iterator for np array, opflag makes not read-only
        for sample in np.nditer(soundArray, op_flags=['readwrite']):
            sample[...] = np.sin(sample)

    return soundArray

def scaleVal(soundArray, scale):
    
    for sample in np.nditer(soundArray, op_flags=['readwrite']):
        sample[...] = sample * scale

    return soundArray


#allows user to choose what theyre doing
while True:
    select = input('Choose 0 for ____ 1 for ___ 2 for ______: ')

    #why can't Python do switch cases aaaah
    if(select == '0'):
        someBool = True
        break

    elif(select == '1'):
        someOtherBool = True
        break

    elif(select == '2'):
        lastBool = True

    else:
        print("Please choose one of the specified options (0/1/2)")

while True:
    fileName = input('Specify .wav file: ')

    if(fileName[-4:] != ".wav"):
        print("Please specify .wav files only")

    else:
        break
    
    
#read in sample file    
sampleRate, data = wavfile.read(fileName)


#do manip


#call function
data = scaleVal(data, -1.5)

#write to test.wav
wavfile.write('test.wav', sampleRate, data)

