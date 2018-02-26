import os
import json
from os  import listdir
from os.path import isfile, join
from rank import compute_BM25
import re

current_directory = os.getcwd()                       
path = os.path.join(current_directory, 'transformed_corpus')
file_names = [f for f in listdir(path) if isfile(join(path, f))]

invertedList = {}
documentLength = {}
totalDocLen = 0
avglen = 0
totaltf = dict()


def get_terms(n): #get all the unique terms in corpus
    global file_names
    gram = n
    global documentLength
    global avglen
    global totalDocLen
    terms = set()
    global totaltf
    totaltf = {}
    for f_name in file_names:
        with open(path+"/"+f_name) as f:
            data = re.split('\W+', f.read(), flags=re.UNICODE)
            documentLength[f_name] = len(data) #storing document length of each document
            print ("document length of "+f_name+" ---> "+str(len(data)))
            totalDocLen += len(data) #calculating total length
            for j in data:
                terms.add(j)
                if j in totaltf.keys(): #generate corpus-wide term frequency
                    totaltf[j] += 1
                else:
                    totaltf.update( { j : 1})
                 
    avglen = totalDocLen/len(documentLength) #calculating average length
    print ("average document length --> "+str(avglen))
    return terms

def get_terms_limited(file_names): #get all the unique terms in corpus
    temptotaltf = {}
    for f_name in file_names:
        with open(path+"/"+f_name) as f:
            data = re.split('\W+', f.read(), flags=re.UNICODE)
            for j in data:
                if j in temptotaltf.keys():
                    temptotaltf[j] += 1
                else:
                    temptotaltf.update( { j : 1})
    return temptotaltf
                 
def generate_inverted_list(gram):
    terms = get_terms(gram)
    print (len(terms))
    for term in terms:
        invertedList[term] = {}
    print ("generating inverted lists ....")
    for docId in file_names:
        with open(path+"/"+docId) as f:

            data1 = []
            data = re.split('\W+', f.read(), flags=re.UNICODE)
            for j in range(len(data) - gram): #generating n-grams. Unigram in this case.
                data1.append(" ".join([str(data[i+j]) for i in range(gram)]))
            for term in data1:
                if not docId in invertedList[term]:
                    invertedList[term][docId] = 0
                invertedList[term][docId] += 1 #document term frequencies
    return invertedList

def generate_qfdict(data): #generating qf dictionary that holds frequency of query terms for BM25
    tempdict = dict()
    for word in data:
        if word in tempdict.keys():
            tempdict[word]+=1
        else:
            tempdict.update( {word : 1} )
    return tempdict

def generate_scores(query): #generates scores for each documents for the query
    data = query.split()
    qfdict = generate_qfdict(data)
    BM25_query_result = {}
    Tfidf_query_result = {}
    Smooth_query_result = {}
    for term in data:
        if term in invertedList:
            doc_dict = invertedList[term] # retrieve index entry
            for docid, freq in doc_dict.items(): #for each document and its word frequency
                BM25_score = compute_BM25(n=len(doc_dict), f=freq, qf=qfdict[term], r=0, N=len(documentLength), dl=documentLength[docid], avdl=avglen)
                if docid in BM25_query_result: #this document has already been scored once
                    BM25_query_result[docid] += BM25_score
                else:
                    BM25_query_result[docid] = BM25_score #this document has not been scored yet
    return BM25_query_result

def getQueries():
    f = open ("transformed_queries.txt", "r") #reading query files
    QueryInput = f.read()
    QueryInput = QueryInput.splitlines()
    Queries = [] #storing query
    Qid = [] #storing query id
    for query in QueryInput:
        temp = query[query.find(" ")+1:] #manipulations to get query
        Queries += [temp]
        Qid += ["Q"+query[:query.find(" ")]] #manipulations to get id
    return Queries, Qid

def writeScores(ScoreDict, Qid, count, system_name, fname, subfoldername): #writing top 100 scores
    filename = os.path.join(os.getcwd(), "Query Results", subfoldername, fname + Qid[count] + ".txt")
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    f = open(filename, "w")
    rank = 0
    for key, value in sorted(ScoreDict.items(), key=lambda kv: kv[1], reverse=True): #sort it by rank
        rank += 1
        f.write(Qid[count] + " Q0 " + key + " " + str(rank) + " " + str(value) + system_name)
        if rank > 100:
            break
    f.close()

def get_topdocs(ScoreDict): #given a BM25 scored document list for a query retrieve top 10 documents
    rank = 1
    topdocs = []
    for key, value in sorted(ScoreDict.items(), key=lambda kv: kv[1], reverse=True): #sort it alphabetically
        rank += 1
        topdocs.append(key)
        if rank > 10:
            break
    return topdocs

def get_topwords(tfdict, common_words): #given a list of words retrive top 5 words removing the common words
    topwords = ""
    rank = 1
    for key, value in sorted(tfdict.items(), key=lambda kv: kv[1], reverse=True): #sort it alphabetically
        if key not in common_words:
            rank += 1
            topwords +=  key + " "
        if rank > 5:
            break
    return topwords

def get_commonwords():
    f = open("common_words.txt", "r")
    data = f.read()
    data = data.splitlines()
    return data

if __name__ == "__main__":
    invertedList = generate_inverted_list(1)
    common_words = get_commonwords()
    query_id = 0
    queries, Qid = getQueries()
    for query in queries:
        #print(query)
        BM25_query_result = generate_scores(query) #calculate BM25 
        BM25_topdocs = get_topdocs(BM25_query_result) #retreive top 10 documents 
        topdict = get_terms_limited(BM25_topdocs) #get a dictionary of all the words and their frequency in our top 10 documents
        top_words = get_topwords(topdict, common_words) #get top 5 words
        query = query + top_words #expand query
        BM25_query_result = generate_scores(query) #calculate BM25 score for expanded query 
        writeScores(BM25_query_result, Qid, query_id, " PRF_BM25_Stopped_CaseFolded_System\n", "PRF-BM25 - ", "PRF") #write scores
        query_id += 1
