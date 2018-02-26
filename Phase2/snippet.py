import os
from os  import listdir
from os.path import isfile, join
# citation 
# http://www.cs.pomona.edu/~dkauchak/ir_project/whitepapers/Snippet-IL.pdf

def snippet():

    #store stop words in a list
    f=open("common_words.txt", "r")
    text=f.read()
    stop= text.split("\n")

    # set window size
    window_size=20

    # get directory for queries
    current_directory = os.getcwd()
    path = os.path.join(current_directory, 'Query Results')

    # get directory for corpus
    directory = os.getcwd()
    filedirectory = directory + "/" + "transformed_corpus"

    f=open("transformed_queries.txt")

    q=1
    # for each query
    for query in f.read().split("\n"):

        # set path for output
        outputfile = "Q" + str(q) + "results.html"
        outputfile = os.path.join(directory, "Results", outputfile)
        print(outputfile)
        if not os.path.exists(os.path.dirname(outputfile)):
            os.makedirs(os.path.dirname(outputfile))

        # Set query id
        temp = query.split()
        temp = "Q" + temp[0]

        # set path for file to be read
        fname = path + "/BM25 - "+temp+".txt"
        tempf = open(fname, "r")
        data = tempf.read()
        data = data.splitlines()
        querytop100resultlist = []

        # Retrieve file names of top 100 results
        for lines in data:
            words = lines.split()
            querytop100resultlist += [words[2]]

        # store query terms in a list
        qlist = query.split()
        qlist=qlist[1:]

        # for each file in top 100 results
        for name in querytop100resultlist:

                # set output directory
                final= filedirectory+"/"+name

                # store words in a file in a list
                f=open(final, "r")
                text=f.read()
                tlist=text.split()
                tlist=tlist[2:-2]

               # initialize variables
                k=-1
                i=0
                max = -1

                # find window with maximum query terms
                while i<len(tlist)+window_size:
                    count=0

                    for word in tlist[i:i+window_size]:
                        if word in qlist and word not in stop:
                            count+=1

                    if count > max:
                        max=count
                        # Store start position of window with most number of query terms in k
                        k=i

                    i+=1

                # save window in snippet
                snippet=""
                i=0
                while i<window_size and i+k< len(tlist):
                    if tlist[k+i] in qlist and tlist[k+i] not in stop:
                        snippet+= "<b>"+tlist[k+i]+"</b>"+ " "
                    else:
                        snippet+=tlist[k+i]+" "
                    i+=1

                #Store output in the file
                f=open(outputfile, "a")
                f.write(name+"<br>..."+snippet+"...<br><br><br>")

        q+=1

snippet()

