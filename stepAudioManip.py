import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
import scipy.signal as signal
import math
import audioop
import tkinter as Tk

def speedUp(soundArray, speedFactor):
#intial idea from http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
#but different implementation, concept is so simple that I don't know how else
#I would go about doing it. As mentioned below this has issues with float so
#using zulko code in function below to do speedchanges currently
 
    #easy usage of step value 
    newArray = soundArray[::speedFactor]

    #TODO: some filtering to make this a smoother change
    
    return newArray

#using floats with simple python range is impossible, this works for speedup
#because its a integer, but slowDown requires a fractional step so we have to
#use numpy's arange (scipy also has an arange)

def speedChange(soundArray, speedFactor):
    
    #step through array with rate defined by our speedfactor
    #factor of .5 means each element shows up twice, etc
    
    newArray = np.arange(0, len(soundArray), speedFactor)
    newArray = newArray[newArray < len(soundArray)].astype(int)
    return soundArray[newArray.astype(int)]

#I could never get this darn thing to work how I wanted and get meaningful results
def sinApply(soundArray, option):
    if(option):
        #np.nditer defines iterator for np array, opflag makes not read-only
        for sample in np.nditer(soundArray, op_flags=['readwrite']):
            sample[...] = np.sin(sample)

    return soundArray

#Multiplying by a scalar does not appear to be a meaningful audio operation,
#unless you want to introduce noise to your audio sample
def scaleVal(soundArray, scale):
    
    for sample in np.nditer(soundArray, op_flags=['readwrite']):
        sample[...] = sample * scale

    return soundArray

#simple little function that exploits Python's slicing syntax to reverse array
def soundReverse(soundArray):

    #the third input to the brackets is the "step" and a negative number means
    #it will start at the end

    newArray = soundArray[::-1]

    #TODO: Filtering that makes this change less harsh

    return newArray

def show_info(aname, a):
    print("Array", aname)
    print("shape", a.shape)
    print("dtype", a.dtype)
    print("min, max: ", a.min(), a.max())
    print()

#this function converts the sound from stereo to mono

def mul_stereo(fileName,width,lfactor,rfactor):
    lsample = audioop.tomono(fileName, width, 1, 0)
    rsample = audioop.tomono(fileName,width, 0, 1)
    lsample = audioop.mul(lsample,width,lfactor)
    rsample = audioop.mul(rsample, width,rfactor)
    lsample = audioop.tostereo(lsample, width, 1, 0)
    rsample = audioop.tostereo(rsample, width, 0, 1)
    return audioop.add(lsample,rsample,width)


#this function cancels the echoes present in the sound
def echocancel(outputdata, inputdata):
    pos = audioop.findmax(outputdata, 800)   # one tenth second
    out_test = outputdata[pos*2:]
    in_test = inputdata[pos*2:]
    ipos, factor = audioop.findfit(in_test,out_test)
    prefill = '\0'*(pos+ipos)*2
    postfill = '\0'*(len(inputdata)-len(prefill)-len(outputdata))
    outputdata = prefill + audioop.mul(outputdata,2-factor) + postfill
    return audioop.add(inputdata, outputdata,2)
    

#allows user to choose what theyre doing, crude but okay for the moment
while True:
    select = input('Choose 0 to reverse, 1 for speed up, 2 for slow down: ')

    #why can't Python do switch cases aaaah
    if(select == '0'):
        reverse = True
        break

    elif(select == '1' or select == '2'):
              
        while True:
            factor = input('Give speed change factor: ')

            #see if input can be made a float
            try:
                factor = float(factor)

            #catch ValueError exception and rather than halting execution, do
            #loop again
            except ValueError:
                print("Invalid input, please give a number value")

                #move to next iteration
                continue

            if(factor < 1):
                print("Please provide a value > 0")

            else:
               break

        if(select == '1'):
            up = True
            
        else:
            down = True
            #invert to get slowdown instead of speedup
            factor = factor ** -1
        break
    
    else:
        print("Please choose one of the specified options (0/1/2)")


while True:
    fileName = input('Specify .wav file: ')

    #checks last 4 character, crude but effective for now
    #should really be some sort of regex or something more robust to be honest
    if(fileName[-4:] != ".wav"):
        print("Please specify .wav files only")
        fileName = input('Specify .wav file: ')

    else:
        break
    
    
#read in sample file    
sampleRate, data = wavfile.read(fileName)

#looking at data

#show_info("data", data)
#sindata = np.sin(data)
#show_info("sindata", sindata)
#scaled = np.round(-32767*sindata)
#show_info("scaled", scaled)
#newdata = scaled.astype(np.int32)
#show_info("newdata", newdata)


#call function
if(select == '0'):
    data = soundReverse(data)

elif(select == '1' or select == '2'):
    data = speedChange(data, factor)
    
    


#write to specified filename
newFile = input("Name the file:")
wavfile.write(newFile, sampleRate, data)


#Clay's work: begin audio visualization data
mpl.use('TkAgg') #set Tk as output for matplotlib

#set up device to receive output from matplotlib plotter ////////////////////////////
root = Tk.Tk() 								#make root window in Tk
root.wm_title("WAV waves") 					#title window
f = Figure(figsize=(5,4), dpi=100) 			#create figure w/ coordinates, pixel size
canvas = FigureCanvasTkAgg(f, master=root) 	#put figure in window and attach to canvas 
canvas.show() 								#show window
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
											#put drawing widget from canvas in window

#open WAV file & initialize variables ///////////////////////////////
afrate,adata = wavfile.read(newFile) #open with read-only functionality
adsize = len(adata)		 	 	#audio data size in frames
#afrate = wf.getframerate() 	 	#audio frame rate
ofrate = 10 				 	#output frame rate
apf = int(afrate/ofrate) 	 	#number of audio frames per output frame
#adata = wf.readframes(adsize) 	#data from file
#wf.close()						#data is extracted, file can be closed

#set data format & unpack
#fmt = '%dh' % (adsize)
#print(adsize)
#adata = struct.unpack(fmt, adata)
#adata = list(adata) #convert from tuple to list

#FUNCTION: get average value of points in a list
def averagepts(points):
	pt_sum = 0
	total = 0
	avg = 0
	for p in points:
		pt_sum += p
		total += 1
	if total != 0:
		avg = int(pt_sum / total)
	return avg

#plot the wave in chunks of frames at a time onto the screen
yhigh = 0
ylow = 0
for i in range(0,adsize,apf) :
	if apf > adsize - i:  #if chunk size is larger than remaining bytes
		apf = adsize - i  #make chunk size smaller to fit

	lastidx = i+apf 			 #index of last frame in chunk
	avgstep = 2 				 #desired number of frames to average
	plt = f.add_subplot(111) 	 #plotter initialization
	avgpts = [] 				 #wave point list initialization
	avgidx = 0
	x = np.arange(0,apf,avgstep) #x-values to plot against wave values

	#fill avgpts with averages of wave values, avgstep number of points at a time
	for j in range(i,lastidx,avgstep):
		if j + avgstep > lastidx:
			avgpts.append(averagepts(adata[j:lastidx]))
			avgidx += 1
		else:
			avgpts.append(averagepts(adata[j:j+avgstep-1]))
			avgidx += 1
		if avgpts[avgidx-1] > yhigh:
			yhigh = avgpts[avgidx-1]
		else:
			if avgpts[avgidx-1] < ylow:
				ylow = avgpts[avgidx-1]

	#plot and render wave on screen//////////////////////
	plt.clear() 			#clear plotter of old points
	if len(x) == len(avgpts) : 
		plt.plot(x,avgpts) 	#plot points
	canvas.draw() 			#render on screen
	plt.set_ylim(ylow,yhigh)

Tk.mainloop()
