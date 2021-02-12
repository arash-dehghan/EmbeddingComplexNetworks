import os
import ast
import sys
sys.path.append('../')
from utils import *

#Setup
graph_name = 'exp1'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [4,8,16,32,64,128]
iterations = 30
seed = 1

#Create graph
os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -seed {seed}')

#Run Experiment
for alg in algorithms:
	for dim in dimensions:
		for _ in range(iterations):
			results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community}').read()
			write_to_csv('results',['algorithm','seed','dim','div','runtime'],[alg, seed, dim]+ ast.literal_eval(results))

