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
dimensions = [4,8,16,32,64,128]
seed = 42
iterations = 10

#Create graph
os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -seed {seed} -d_max 464')

#Run Experiment
for alg in algorithms:
	for dim in dimensions:
		for i in range(iterations):
			results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community} -representation_size {dim}').read()
			write_to_csv('results',['algorithm','seed','dim','acc','div','runtime'],[alg, seed, dim, acc_score(community,'result.embedding',i)] + ast.literal_eval(results))
