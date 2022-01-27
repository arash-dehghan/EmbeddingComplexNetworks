import os
import ast
import sys
sys.path.append('../')
from utils import *

#Setup
graphs = ['mousebrain', 'emaileu', 'github', 'airport']
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [4,8,16,32,64,128]
iterations = 30

#Run Experiment
for graph in graphs:
	edgelist = f'../../data/{graph}/{graph}.edgelist'
	community = f'../../data/{graph}/{graph}.community'
	for alg in algorithms:
		for dim in dimensions:
			for _ in range(iterations):
				results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community} -representation_size {dim}').read()
				write_to_csv('results',['algorithm','seed','dim','graph','div','runtime'],[alg, -1, dim, graph]+ ast.literal_eval(results))
