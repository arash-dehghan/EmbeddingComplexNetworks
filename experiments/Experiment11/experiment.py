import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp11'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [4,8,16,32,64,128]
seed = 1
iterations = 10

#Create graph
os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -communitysizesfile {community_sizes} -d_max 464 -seed {seed}')

#Run Experiment
for alg in algorithms:
	for dim in dimensions:
		for i in range(iterations):
			G, edges, reduced = remove_random_edges(edgelist,i)
			results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {reduced} -community {community} -representation_size {dim}').read()
			auc, acc = auc_score(G,edges,'result.embedding',i)
			write_to_csv('results',['algorithm','seed','dim','auc','acc','div','runtime'],[alg, seed, dim, ]auc, acc + ast.literal_eval(results))
