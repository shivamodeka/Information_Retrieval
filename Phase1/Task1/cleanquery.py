import os
from bs4 import BeautifulSoup
from os import listdir
from string import punctuation
import re

def clean():

    file = "cacm.query.txt" # query file
    f=open(file, "r")
    text=f.read() # read the content from file

    soup = BeautifulSoup(text, "lxml") # using BeautifulSoup to scrap the content

    fs="" # storing clean content

    for item in soup.find_all("doc"):
        s=item.extract() # extracting  relevant content from doc tag
        for c in s.get_text():
            if c == "\n": # handling new lines
                fs=fs+ " "
            else:
                fs = fs + c
        fs=fs+"\n"

    fs=fs.lower()
    data = fs


    # handling the punctuations
    remove_punc = re.compile('[\.,;\*+/!@#$%^&:\(\)\?"\']') # regular expressions to compile all punctuations

    p = re.compile('(\d+)\.(\d+)') # regular expressions to handle all decimals between digits
    data = p.sub(r'\1*\2', data)

    data = re.sub(remove_punc, '', data)

    replace_dots = re.compile('\*\*')
    data = re.sub(replace_dots, '.', data)

    data = data.splitlines()
    newdata = []
    for line in data:
        line = line[2:]
        lines = (line.strip() for line in line.splitlines()) # remove space on each lines
        linebreakchunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # get chunks of newlines
        text = ' '.join(linebreakchunk for linebreakchunk in linebreakchunks if linebreakchunk)
        newdata.append(text)


    f=open("transformed_queries.txt", "w") # writing content into respective files
    for line in newdata:
        f.write(line)
        f.write("\n")
    f.close()


clean()
