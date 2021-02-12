import os
import csv
import pandas as pd 
import igraph as ig
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_mutual_info_score as AMI

def readEmbedding(fn="_embed", N2K=None):
	D = pd.read_csv(fn, sep=' ', header=None)
	# D = D.dropna(axis=1)
	if N2K!=None:
		x = [N2K[i] for i in D[0]]
		D[0] = x    
		D = D.sort_values(by=0)
	Y = np.array(D.iloc[:,1:])
	return Y

def write_to_csv(csv_file,csv_header,csv_results):
	csv_file = f'{csv_file}.csv'
	csv_exists = os.path.exists(csv_file)
	with open(csv_file,'a') as resultFile:
		if csv_exists == False:
			wr = csv.writer(resultFile, dialect='excel')
			wr.writerow(csv_header)
		wr = csv.writer(resultFile, dialect='excel')
		wr.writerow(csv_results)

def ami_score(edgelist,community,embedding):
	G = ig.Graph.Read_Ncol(edgelist,directed=False)
	c = np.loadtxt(community,dtype='uint16',usecols=(0))
	G.vs['comm'] = [c[int(x['name'])] for x in G.vs]

	X = readEmbedding(fn=embedding)
	GT = {k:(v) for k,v in enumerate(G.vs['comm'])}

	k = 5
	cl = KMeans(n_clusters=k).fit(X)
	d = {k:v for k,v in enumerate(cl.labels_)}
	return AMI(list(GT.values()),list(d.values()))

	