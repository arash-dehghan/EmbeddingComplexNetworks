import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp4'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [32,64,128]
gammas = [2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
iterations = 10

#Run Experiment
seed = 1
for gamma in gammas:
	for i in range(iterations):
		#Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -communitysizesfile {community_sizes} -t1 {gamma} -seed {seed}')
		for alg in algorithms:
			for dim in dimensions:
				for _ in range(iterations):
					results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community}').read()
					write_to_csv('results',['algorithm','seed','dim','gamma','div','runtime'],[alg, seed, dim, gamma] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')
