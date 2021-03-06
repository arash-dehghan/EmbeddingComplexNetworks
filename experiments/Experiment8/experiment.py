import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp8'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [32,64,128]
deltas = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
iterations = 10

#Run Experiment
seed = 0
for delta in deltas:
	for i in range(iterations):
		#Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -communitysizesfile {community_sizes} -d_max {int(10000**delta)} -seed {seed}')
		for alg in algorithms:
			for dim in dimensions:
				for _ in range(iterations):
					results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community}').read()
					write_to_csv('results',['algorithm','seed','dim','delta','div','runtime'],[alg, seed, dim, delta] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')
