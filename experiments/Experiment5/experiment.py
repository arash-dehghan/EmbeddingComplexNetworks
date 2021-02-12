import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp5'
degreefile = '../degrees.txt'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
dimensions = [4,8,16,32,64,128]
pq_vals = [[1.0,1.0],[1.0,3.0],[1.0,5.0],[1.0,7.0],[1.0,9.0],[1.0,1.0/3.0],[1.0,1.0/5.0],[1.0,1.0/7.0],[1.0,1.0/9.0],[3.0,1.0],[5.0,1.0],[7.0,1.0],[9.0,1.0],[1.0/3.0,1.0],[1.0/5.0,1.0],[1.0/7.0,1.0],[1.0/9.0,1.0]]
iterations = 10

#Run Experiment
seed = 1
for pq in pq_vals:
	for i in range(iterations):
		# Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -degreefile {degreefile} -communitysizesfile {community_sizes} -seed {seed}')
		for dim in dimensions:
			for _ in range(iterations):
				results = os.popen(f'python3 ../../src/main.py -algorithm node2vec -edgelist {edgelist} -community {community} -p {pq[0]} -q {pq[1]}').read()
				write_to_csv('results',['algorithm','seed','dim','p','q','div','runtime'],[alg, seed, dim, pq[0], pq[1]] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')