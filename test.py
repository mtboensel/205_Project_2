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
    
sampleRate, data = wavfile.read('creak.wav')


data = trigApply(data, 1)

wavfile.write('test.wav', sampleRate, data)

