import os
import ast
import sys
sys.path.append('../')
from utils import *
import random

#Setup
graph_name = 'exp50k'
edgelist = f'../../data/{graph_name}/{graph_name}.edgelist'
community = f'../../data/{graph_name}/{graph_name}.community'
algorithms = ['node2vec','hope','deepwalk','line','sdne','verse']
dimensions = [4,8,16,32,64,128]
iterations = 2
seed = 0
rng = random.randint(1,10**20)
#Create graph
os.system(f'python3 ../../src/ABCD/ABCD.py -name {graph_name} -communitysizesfile generate -n 50000 -d_max 1357 -seed {seed}')

#Run Experiment
for alg in algorithms:
	for dim in dimensions:
		for _ in range(iterations):
			results = os.popen(f'python3 ../../src/main.py -algorithm {alg} -edgelist {edgelist} -community {community} -representation_size {dim} -l 450 -workers 24').read()
			write_to_csv(f'/home/results50k/results_{rng}',['algorithm','seed','dim','div','runtime'],[alg, seed, dim]+ ast.literal_eval(results))

