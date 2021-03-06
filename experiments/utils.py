import os
import csv
import pandas as pd
import numpy as np
import igraph as ig
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_mutual_info_score as AMI, roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split
import xgboost as xgb

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

def acc_score(community,embedding,seed):
	X = readEmbedding(fn=embedding)
	y = np.loadtxt(community,dtype='uint16',usecols=(0))
	# Split dataset with 75/25 ratio and fixed seed
	X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.25, random_state=seed)
	# Train XGBoost Classifier
	clf = xgb.XGBClassifier(objective='multi:softmax', random_state=seed)
	clf.fit(X_train, y_train)
	return sum(y_test == clf.predict(X_test))/y_test.shape[0]

def remove_random_edges(edgelist,seed):
	G = ig.Graph.Read_Ncol(edgelist, directed=False)
	test_size = int(np.round(.1*G.ecount()))
	np.random.seed(seed)
	test_eid = np.random.choice(G.ecount(), size=test_size, replace=False)
	edges = [(G.es[eid].source, G.es[eid].target) for eid in test_eid]
	removed_edges = f"{edgelist}_removed"
	with open(removed_edges, "w") as f:
		for vid in edges:
			f.write(str(vid[0])+" "+str(vid[1])+"\n")
	Gp = G.copy()
	Gp.delete_edges(test_eid)
	reduced_graph = f"{edgelist}_reduced"
	Gp.write(reduced_graph, format="edgelist")
	return G, edges, reduced_graph

def auc_score(G,edges,embedding,seed):
	# features for node pairs without edges
	ctr = 0
	counter = 0
	nonedges = []
	while ctr < len(edges):
		np.random.seed(seed+counter+1)
		e = np.random.choice(G.vcount(), size=2, replace=False)
		if G.get_eid(e[0], e[1], directed=False, error=False) == -1:
			nonedges.append((e[0], e[1]))
			ctr += 1
		counter += 1
	X = readEmbedding(fn=embedding)
	edges_dist = [np.linalg.norm(X[e[0]]-X[e[1]]) for e in edges]
	nonedges_dist = [np.linalg.norm(
		X[e[0]]-X[e[1]]) for e in nonedges]
	true_y = [1]*len(edges)+[0]*len(nonedges)
	score = np.array(edges_dist+nonedges_dist)
	score = 1-score/np.max(score)
	return roc_auc_score(true_y, score), accuracy_score(true_y, score > np.median(score))
