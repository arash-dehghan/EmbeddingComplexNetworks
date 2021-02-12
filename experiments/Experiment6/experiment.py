import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp6'
degreefile = '../degrees.txt'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
dimensions = [4,8,16,32,64,128]
walks = [[40,10],[80,10],[160,10],[80,5],[80,20]]
iterations = 10

#Run Experiment
seed = 1
for walk in walks:
	for i in range(iterations):
		# Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -degreefile {degreefile} -communitysizesfile {community_sizes} -seed {seed}')
		for dim in dimensions:
			for _ in range(iterations):
				results = os.popen(f'python3 ../../src/main.py -algorithm node2vec -edgelist {edgelist} -community {community} -walk-length {walk[0]} -number-walks {walk[1]}').read()
				write_to_csv('results',['algorithm','seed','dim','walk_length','number_walks','div','runtime'],[alg, seed, dim, walk[0], walk[1]] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')