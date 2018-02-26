import re
import sys
import requests
import codecs
import os
from bs4 import BeautifulSoup
import unicodedata
from os.path import isfile, join
from os import listdir

current_directory = os.getcwd()    # get the current directory
path = os.path.join(current_directory, 'cacm') # change path to current directory/cacm
file_names = [f for f in listdir(path) if isfile(join(path, f))] # get all files from cacm

def parse():
        global path
        for f_name in file_names:
            with codecs.open(path+"/"+f_name) as f: # iterate through each file
                 res = f.read() # read the content
                 res = res.lower() # case-fold
                 data = res
                 data = data.split()
                 data = " ".join(data) #form a single content

                 #handling the punctuations
                 remove_punc = re.compile('[\.,;!@#$%^&\(\)\?"\']')

                 p = re.compile('(\d+)\.(\d+)') # handle decimals between digits
                 data = p.sub(r'\1*\2',data)

                 data = re.sub(remove_punc, '', data) # remove punctuations

                 replace_dots = re.compile('\*')
                 data = re.sub(replace_dots, '.', data)

                 f_name1 = ".txt".join(f_name.split(".html")) # write clean content into the respective text file
                 current_directory = os.getcwd()
                 f_name1 = os.path.join(current_directory, 'transformed_corpus', f_name1) # path of transformed  corpus 
                 print(f_name1)
                 if not os.path.exists(os.path.dirname(f_name1)):
                    os.makedirs(os.path.dirname(f_name1))
                 f = codecs.open(f_name1, "w", encoding = 'utf-8')
                 f.write(data)
                 f.close()


def main():
    parse() # for punctuation handling

main()
