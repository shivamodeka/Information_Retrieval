import os
from os  import listdir
from os.path import isfile, join


def makecorpus(): #make stemmed corpus
    current_directory = os.getcwd()                       
    path = os.path.join(current_directory, 'stemmed_corpus')
    f = open("cacm_stem.txt", "r")
    data = f.read()
    while data.find("#") != -1: #while there exsits a new file
        first = data.find("#")
        data = data[first+2:]
        filedata = data[:data.find("#")-1]
        filedata = filedata.splitlines()
        filename = path + "/CACM - " + filedata[0] + ".txt" #make a new file for each document
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        f1 = open(filename, "w")
        filedata = filedata[1:]
        for line in filedata:
            f1.write(line) #write conents
            f1.write("\n")
        f1.close() #close file
        data = data[data.find("#")-1:] #go to next file