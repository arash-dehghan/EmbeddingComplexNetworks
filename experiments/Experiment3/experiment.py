import os
import ast
import sys
import shutil
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp3'
degreefile = '../degreesExp3.txt'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [32,64,128]
betas = [1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]
iterations = 10

#Run Experiment
seed = 0
for beta in betas:
	for i in range(iterations):
		#Create Graph
		os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -degreefile {degreefile} -t2 {beta} -seed {seed}')
		for alg in algorithms:
			for dim in dimensions:
				for _ in range(iterations):
					results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community} -representation_size {dim}').read()
					write_to_csv('results',['algorithm','seed','dim','beta','div','runtime'],[alg, seed, dim, beta] + ast.literal_eval(results))
		seed+=1
		shutil.rmtree(f'../../data/{graph_name}')
