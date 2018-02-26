import os
import json
from os  import listdir
from os.path import isfile, join
from rank import compute_BM25
from rank import compute_tfidf
from rank import compute_smooth
from corpus import parse
from cleanquery import clean
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
    for f_name in file_names:
        with open(path+"/"+f_name) as f:
            data = re.split('\W+', f.read(), flags=re.UNICODE)
            documentLength[f_name] = len(data) #storing document length of each document
            print ("document length of "+f_name+" ---> "+str(len(data)))
            totalDocLen += len(data) #calculating total length
            for j in data:
                terms.add(j)
                if j in totaltf.keys(): #genrate corpus-wide term frequency
                    totaltf[j] += 1
                else:
                    totaltf.update( { j : 1})
                 
    avglen = totalDocLen/len(documentLength) #calculating average length
    print ("average document length --> "+str(avglen))
    return terms

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
    corpuslen = 0
    for docid in documentLength.keys():
        corpuslen += documentLength[docid]
    for term in data:
        if term in invertedList:
            doc_dict = invertedList[term] # retrieve index entry
            for docid, freq in doc_dict.items(): #for each document and its word frequency generate BM25 score, TFIDF score and Smooth Query likleyhood model score
                BM25_score = compute_BM25(n=len(doc_dict), f=freq, qf=qfdict[term], r=0, N=len(documentLength), dl=documentLength[docid], avdl=avglen)
                TFIDF_score = compute_tfidf(n=len(doc_dict), f=freq, N=len(documentLength), dl=documentLength[docid]) # calculate score
                SM_score = compute_smooth(lam=0.35, f=freq, dl=documentLength[docid], N=corpuslen, fc=totaltf[term])
                if docid in BM25_query_result: #this document has already been scored once
                    BM25_query_result[docid] += BM25_score
                    Tfidf_query_result[docid] += TFIDF_score
                    Smooth_query_result[docid] *= SM_score
                else:
                    BM25_query_result[docid] = BM25_score #this document has not been scored yet
                    Tfidf_query_result[docid] = TFIDF_score
                    Smooth_query_result[docid] = SM_score
    return BM25_query_result, Tfidf_query_result,Smooth_query_result

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
        if rank > 99:
            break
        f.write("\n")
    f.close()

if __name__ == "__main__":
    parse()
    clean()
    invertedList = generate_inverted_list(1)
    query_id = 0
    queries, Qid = getQueries()
    for query in queries: #for each query
        BM25_query_result, TFIDF_query_result, Smooth_query_result = generate_scores(query) #generate 3 scores
        writeScores(BM25_query_result, Qid, query_id, " BM25_QNotStopped_CaseFolded_System", "BM25 - ", "BM25") #write 3 scores
        writeScores(TFIDF_query_result, Qid, query_id, " TFIDF_QNotStopped_CaseFolded_System", "TFID - ", "TFIDF")
        writeScores(Smooth_query_result, Qid, query_id, " Smooth_QNotStopped_CaseFolded_System", "Smooth - ", "SMOOTH")
        query_id += 1
