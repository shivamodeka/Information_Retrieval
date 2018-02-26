from math import log

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

# where:  n -> no. of documents containing the term i
	#         f -> frequency of the term i in the document
	#        qf -> frequency of term i in the query
	#         r -> relevance i.e = 0
	#         N -> number of documents on the collection i.e = 1000
	#        dl -> document length
	#      avdl -> avg. document length


def compute_BM25(n, f, qf, r, N, dl, avdl):
	K = compute_K(dl, avdl)
	first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)))
	second = ((k1 + 1) * f) / (K + f)
	third = ((k2+1) * qf) / (k2 + qf)
	return first * second * third

def compute_tfidf(n, f, N, dl):
	tf = f / dl
	idf = log(N/n)
	return tf * idf

def compute_smooth(lam, f , dl, N, fc):
	first = (1-lam) * (f/dl)
	second = lam * (fc / N)
	return first * second

def compute_K(dl, avdl):
	return k1 * ((1-b) + b * (float(dl)/float(avdl)) )
