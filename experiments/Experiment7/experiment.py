import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp7'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [32,64,128]
ns = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
iterations = 10

#Run Experiment
seed = 1
for n in ns:
	for i in range(iterations):
		#Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -n {n} -seed {seed}')
		for alg in algorithms:
			for dim in dimensions:
				for _ in range(iterations):
					results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community}').read()
					write_to_csv('results',['algorithm','seed','dim','n','div','runtime'],[alg, seed, dim, n] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')
