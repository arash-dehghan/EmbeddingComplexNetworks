import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp10'
degreefile = '../degrees.txt'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [4,8,16,32,64,128]
seed = 1
iterations = 10

#Create graph
os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -degreefile {degreefile} -communitysizesfile {community_sizes} -seed {seed}')

#Run Experiment
for i in range(iterations):
	for alg in algorithms:
		for dim in dimensions:
			for _ in range(iterations):
				results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community} -representation_size {dim}').read()
				write_to_csv('results',['algorithm','seed','dim','ami','div','runtime'],[alg, seed, dim, ami_score(edgelist,community,'result.embedding')] + ast.literal_eval(results))
