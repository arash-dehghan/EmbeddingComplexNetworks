import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp2'
degreefile = '../degrees.txt'
community_sizes = '../community_sizes.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [32,64,128]
xis = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
iterations = 10

#Run Experiment
seed = 1
for xi in xis:
	for i in range(iterations):
		#Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -degreefile {degreefile} -communitysizesfile {community_sizes} -xi {xi} -seed {seed}')
		for alg in algorithms:
			for dim in dimensions:
				for _ in range(iterations):
					results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community}').read()
					write_to_csv('results',['algorithm','seed','dim','xi','div','runtime'],[alg, seed, dim, xi] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')
