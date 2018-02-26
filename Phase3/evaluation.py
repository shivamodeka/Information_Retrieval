import os
from os  import listdir
from os.path import isfile, join, isdir

class relevance_score: #data structure for holding document id given a rank, precsion at that rank and recall at the rank
    def __init__(self, docname, pp, rr):
        self.name = docname
        self.pr =   pp
        self.rr =   rr

def getreldict(): #read relevant document text file and generate dictionary that holds query id and list of relevant documents
    f = open("cacm.rel.txt", "r")
    data = f.read()
    data = data.splitlines()
    reldict = dict()
    for line in data:
        words = line.split()
        if words[0] in reldict.keys():
            reldict[words[0]] += [words[2]+".txt"]
        else:
            reldict.update( { words[0] : [words[2]+ ".txt"]  })
    return reldict

def generate_precisionrecalltable(folder, data, query, docpr, docrr, klist, fileevaldict): #write the table of Precision, Recall, AP for the query of that system, RR of the query, K@5 an K@20
    evalfile = os.path.join(os.getcwd(), "Evaluation", "Eval-"+folder, data[0].split()[5]+"-Q"+query+".csv") 
    if not os.path.exists(os.path.dirname(evalfile)):
        os.makedirs(os.path.dirname(evalfile))
    newfile = open(evalfile, "w")
    newfile.write("Query Average PR :," + str(docpr) + "\n")
    newfile.write("Query RR :," + str(docrr) + "\n")
    for k in klist:
        newfile.write("P@"+k+","+str(fileevaldict[k].pr)+"\n")
    newfile.write("Rank,Filname, Precision, Recall\n")
    for key,obj in sorted(fileevaldict.items(), key = lambda kv: int(kv[0]), reverse=False):
        newfile.write(key+ ","+ obj.name + "," + str(obj.pr) + "," + str(obj.rr) + "\n")
    newfile.close()
    
def generate_systemMARMRR(docevaldict, queries_with_rel_documents): 
    mpr = 0
    mar = 0
    count = 0
    for key in docevaldict.keys(): #for each document's AP and RR get the sum.
        temp = docevaldict[key]
        mpr += temp[0]
        mar += temp[1]
    mpr = mpr / queries_with_rel_documents #divide sum of AP by number of queries who's relevant document we have
    mar = mar / queries_with_rel_documents #divide sum of RR by number of queries who's relevant document we have
    return mpr, mar

def get_file_eval(reldict, dir, filelist, folder, klist): #generate system level MPR and MAR and also calculate precision and recall for each query result file
    docevaldict = {} # holds MAP an MAR for each query file for the given system
    for item in filelist: #for all files of given system
        if dir.find("LUCENE") == -1: #java output txt file couldnt be read using default encoding hence special encoding for lucene system
            f = open( dir + "/" + item, "r")
        else:
            f = open(dir + "/" + item, "r" , encoding='windows-1252')
        data = f.read() #read data
        data = data.splitlines()
        tempdict = {}
        currentp = 0
        currentr = 0
        count = 0
        query = data[0].split()[0][1:]
        if query not in reldict.keys(): #if no relevant documents are given for the given queryid we skip processing
            continue
        totalr = len(reldict[query]) #total relvant documents
        mtotalp = 0 
        fileevaldict = {} #dictionary for holding the query's recall and precision
        tempcount = 0
        docrr = 0 #for holding document's RR
        for line in data:
            words = line.split()
            count += 1
            if words[2] in reldict[query]: #if the document is in relevant document
                tempcount += 1 
                currentp += 1 #increase precision's numerator by 1
                currentr += 1 # increase recall's numerator by 1
                pr = currentp / count # get precision based on current rank
                rr = currentr / totalr # get recall
                mtotalp += pr
                if currentp == 1: # if it's the first precision
                    docrr = 1/count # get RR
            else:
                pr = currentp / count # get precsion based on rank
                rr = currentr / totalr # get recall based on rank
            fileevaldict.update( { words[3] : relevance_score(words[2], pr, rr) }) #store rank, documentid, pr and recall
        if tempcount == 0:
            docpr = 0 #if no relevant documents are found documents mean precission is 0
        else:    
            docpr = mtotalp / tempcount #otherwise documents mean precision is sum of all precision values divided by total number of relevant documents found for that query
        if item not in docevaldict.keys():
            docevaldict.update( { item : [docpr, docrr] }) #update our dictionary for holding given query's MAP and MAR
        generate_precisionrecalltable(folder, data, query, docpr, docrr, klist, fileevaldict) #generate tables for each query result file
    mpr, mar = generate_systemMARMRR(docevaldict, len(reldict.keys())) #generate MPR and MAR for each system
    return mpr, mar, data[0].split()[5]

def get_folderlist(): #get folder;s of different system.
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, 'Query Results')
    onlyfolders = [f for f in listdir(final_directory) if isdir(join(final_directory, f))]
    if 'DS_Store' in onlyfolders:
        onlyfolders.remove('.DS_Store')
    return onlyfolders, current_directory, final_directory

def get_filelist(final_directory, folder): #get query result file of each system
    curr_dir = os.path.join(final_directory, folder)
    print(curr_dir)
    onlyfiles = [f for f in listdir(curr_dir) if isfile(join(curr_dir, f))]
    if 'DS_Store' in onlyfiles:
        onlyfiles.remove('.DS_Store')
    return onlyfiles, curr_dir

def init_finalevalreport_file(current_directory): #initialize a file for our overall report
    ffname = os.path.join(current_directory, "Evaluation" , "Overall.csv")
    if not os.path.exists(os.path.dirname(ffname)):
            os.makedirs(os.path.dirname(ffname))
    finalfile = open(ffname, "w")
    print(ffname)
    return finalfile


def start():
    klist=['5','20'] #for printing P@K
    reldict = getreldict() #dictionary holding query id and the list of documents that are relevant
    onlyfolders, current_directory, final_directory = get_folderlist() #get list of all different system's result folder
    finalfile = init_finalevalreport_file(current_directory) #overall reportfile object 
    finalfile.write("Filename,MAP,MRR\n")
    for folder in onlyfolders:
        onlyfiles, curr_dir = get_filelist(final_directory,folder) #get all the query result for each system 
        mpr, mar, filename = get_file_eval(reldict, curr_dir, onlyfiles, folder, klist) #calculate score for each document of that system and system's MAP and MAR
        finalfile.write(filename + "," + str(mpr) + "," + str(mar)+"\n") #write the system's MAP and MAR to  overall report file
    finalfile.close()

start()