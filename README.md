# Information_Retrieval
Search Engine

All the programs in the project, except for Lucene are written in python version 3.4
All programs are compiled and run using the format -> python program_name.py, where program_name.py is the program to be executed.
The programs do not require user input. The required files are fetched from the current directory of execution.
The task wise set up and compilation of the project is as follows:

*** Phase 1 ***

* Task 1 *

All the files for this task are in the Task1 folder in Phase1.
The main program for this task is score.py. 
It internally makes a call to the programs corpus.py and cleanquery.py that transform the provided corpus and cleans the provided queries and generate the respective files at the same destination. 
It then generates the results for BM25, tf-idf and smoothed query likelihood model in the query results folder. No relevance judgements used.

Files that need to be present in the same folder :  1. cacm  (corpus folder) 
                                                    2. cacm.query.txt (corpus query file) 
                                                    3. cleanquery.py 
                                                    4. corpus.py 
                                                    5. rank.py
Output files :  1. transformed queries.txt (Casfolded and punctuation removed queries)  
                2. transformed corpus (folder for storing punctuation removed and case folded corpus) 
                3. Query Results (Query result of each of the 3 models)

The folder already contains the cacm and cacm.query.txt along with the source codes.
The java source code and the results for the lucene model are in the Task1_Lucene folder.

* Task 2 *

All the files for this task are in the Task2 folder in Phase1.

The task takes the transformed corpus and the cleaned queries generated in Task1.
prf.py contains the source code to perform pseudo relevance feedback on BM25.
The results are generated in query results folder.

Files that need to be present in the same folder :  1. transformed queries.txt (Casfolded and punctuation removed queries) 
                                                    2. transformed corpus (folder for storing punctuation removed and case folded corpus)
                                                    3. common_words.txt
Output files : 1. Query Result (folder that holds PRF generated query reuslts)

* Task 3 *

Task 3 is sub-divided into two tasks: Stemmed and Stopped.

1. Stemming - 
makestemmedcorpus.py generates the stemmed corpus from the cacm_stem.txt.
stemmedscore.py retrieves the results into Query Results.

Files that need to be present in the same folder :  1. cacm_stem.query.txt
                                                    2. cacm_stem.txt
                                                    3. makestemmedcorpus.py
Output files :  1. stemmed_corpus (for storing stemmed corpus)
                2. Query Result (for storing query results)

2. Stopping -
the program stoppedscore.py retrieves the results for the queries by stopping the terms in the common_words.txt file.

Files that need to be present in the same folder :  1. transformed queries.txt (Casfolded and punctuation removed queries) 
                                                    2. transformed corpus (folder for storing punctuation removed and case folded corpus)
                                                    3. common_words.txt
Output files : 1. Query Result (folder that holds PRF generated query reuslts)

** Phase 2 **

snippet.py generates the snippets in phase 2. It takes the query results from the folder Query Results and generates html files for each query (with snippets) in the Results folder.

Files that need to be present in the same folder :  1. transformed queries.txt (Casfolded and punctuation removed queries) 
                                                    2. transformed corpus (folder for storing punctuation removed and case folded corpus)
                                                    3. Query_Results (holds all the query file)
Output files : 1. Result (folder that holds .html file for the snippets that is generated for each query)

** Phase 3 **

The program evaluation.py performs Phase 3.
The folder Query Results contains all the results from the eight distinct runs.
The evaluation results/tables from these runs are in Evaluation folder in respective directories.
Overall.csv in Evaluation displays the final table.

Files that need to be present in the same folder :  1. cacm.rel.txt
                                                    2. Query Results (A folder that holds all the queries that need to be evaluated)
Output files : 1. Evaluation folder (Generates evaluation tables in csv format that holds RR & APR for each file and an overall file that generates overall result for all the systems)


** File Formats **

1. Query Result -
This folder holds a directory with the name as the System that has been used and inside it are all the 64 query results. For example all the BM25 generated query result will be stored in a folder
called BM25 inside query result.

2. Result - (Phase 2)
This folder is used to hold HTML files of snippet that is generated for each query present in the query file.

3. <system_name> - Q1. txt
This holds top 100 results of a system for the query with ID Q1.
Format of this file is :-

<queryID> Q0 <docId> <rank> <score> <full_system_name>
Example -
Q1 Q0 CACM-1657.txt 1 25.879483432489558 BM25_QNotStopped_CaseFolded_System

4. Evaluation (Phase 3)

This folder generated at the end of phase 3 holds evaulation file for each of the system folder present in Query Result.

For example -
Eval-BM25 folder will have evaulated query results for each of the query files present in BM25 folder in Query Result

Naming convention of each file is -
<full_system_name>-Q1.csv

Example
BM25_QNotStopped_CaseFolded_System-Q1.csv

File Format :-
First line contatins Average Precision for that table.
Second line contains Reciprocal rank
Third and Fourth line contain P@5 and P@20 respectively
And then the table is given in the format 
Rank	Filname	    Precision	 Recall
1	CACM-1657.txt	    0	        0



**END**   
