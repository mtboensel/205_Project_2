# 205_Project_2

Team : NP-Complete

Members: Matthew Boensel, Ulysses Vega and Philip Evans

Summary: 
This project is meant to use Python towards some sort of multimedia purpose.  Our aim is to manipulate audio.  While 
Python provides a wide variety of libraries for this purpose, we are currently using numPy, sciPy, Math, matplotlib, tkinter, and audioop.  We came to these libraries after a number of difficulties while trying to use PyAudio and Pysox, among others.

Our long-term goal is to take audio input, perform some sort of tranformation on it (should the user deem it neccessary),
and then provide a visual representation of the result of whatever operations (if any) we performed.  Currently, the 
program has only basic functionality- allowing for the reversal of a sound sample or a change in time scale, which is then visualized as a wave.  The filters are acheived by performing transformations on the numPy arrays that hold the audio samples. It was our intent to implement more functionality, such as a low-pass filter or other types of visualizations, but that proved out of reach for the time being. If we chose to move forward with this project, our goal would be to include some more meaningful tranformations on the audio samples, as well as to implement more visualizations.
