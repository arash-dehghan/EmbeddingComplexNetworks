import argparse
import ast
import os
import igraph as ig
import numpy as np
from inspect import getsourcefile
from datetime import datetime
import pandas as pd

class Embedding(object):
	def __init__(self, embedding_path: str, dimensions: int, index_path: str = None):
		self.dimensions = dimensions
		self.embeddings = self.load_embeddings(embedding_path)
		self.index: Dict[str, int] = {}
		if index_path:
			self.load_index(index_path)

	def load_embeddings(self, file_name: str) -> np.ndarray:
		embeddings = np.fromfile(file_name, dtype=np.float32)
		length = embeddings.shape[0]
		assert length % self.dimensions == 0, f"The number of floats ({length}) in the embeddings is not divisible by" \
											  f"the number of dimensions ({self.dimensions})!"
		embedding_shape = [int(length / self.dimensions), self.dimensions]
		embeddings = embeddings.reshape(embedding_shape)
		return embeddings

	def load_index(self, index_path: str) -> None:
		print("Loading uri index...")
		with open(index_path, "r") as file:
			for line in [line.strip() for line in file.readlines()]:
				index, uri = line.split(",", 1)
				self.index[uri] = int(index)
		print(f"Done loading {len(self.index)} items.")

	def __getitem__(self, item) -> np.ndarray:
		if self.index and isinstance(item, str):
			return self.embeddings[self.index[item]]
		return self.embeddings[item]
		
def cluster(filename,type):
	with open(filename,'r') as f:
		edges = [tuple(map(int, i.split(' '))) for i in f]
	g = ig.Graph.TupleList(edges)
	idx = np.argsort(g.vs['name'])
	if type == 'louvain':
		m = g.community_multilevel().membership
	else:
		m = g.community_ecg(min_weight=.5).membership
	ml = [m[i] for i in idx]
	with open(filename.replace('edgelist','community'),'w') as f:
		f.write('\n'.join(str(x) for x in ml))
		
def buildGraph(edge_file, comm_file):
	comm = pd.read_csv(comm_file, sep=r'\s+', header=None)[0].tolist()
	E = pd.read_csv(edge_file, sep=r'\s+', header=None)
	x = min(E.min())
	E = np.array(E-x) ## make everything 0-based
	n = len(comm)
	E = np.array([x for x in E if x[0]<x[1]]) ## simplify
	cl = ['magenta','grey','green','cyan','yellow','red','blue','tan','gold']
	pal = ig.RainbowPalette(n=max(comm)+1)
	v = [i for i in range(n)]
	g = ig.Graph(vertex_attrs={"label":v}, edges=list(E), directed=False)
	g['min']=x
	g.vs["color"] = [pal.get(i) for i in comm]
	g.vs['comm'] = comm
	return g

def save_as_n2v(Y, outfile, min_node):
	n = Y.shape[0]
	dim = Y.shape[1]
	h = str(n) + ' ' + str(dim)
	with open(outfile,'w') as fn:
		fn.write("%s\n" % h)
		for i in range(n):
			fn.write("%s" % str(i+min_node))
			for j in range(dim):
				fn.write(" %s" % str(Y[i][j]))
			fn.write("\n")
			
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='N2V embedder')
	parser.add_argument('-algorithm', '--algorithm', type=str, choices=['node2vec','hope','deepwalk','line','sdne','verse'], required=True)
	parser.add_argument('-edgelist', '--edgelist', type=str, required=True)
	parser.add_argument('-community', '--community', type=str, default=None)
	parser.add_argument('-l', '--l',type=int, default=200, help='Number of landmarks to create')
	parser.add_argument('-f', '--f',type=int, default=0, help='Number of forced landmarks to be created')
	parser.add_argument('-m', '--m', choices = ['rss', 'rss2', 'size', 'diameter'], default='diameter', help='Chosen ladnmark creation method')
	parser.add_argument('-clustering', '--clustering', choices = ['ecg', 'louvain'], default='ecg', help='Clustering used')
	parser.add_argument('-number-walks', '--number_walks', type=int, default=10, help='The number of random walks to start at each node; the default is 10;')
	parser.add_argument('-walk-length', '--walk_length', type=int, default=80, help='The length of random walk started at each node; the default is 80;')
	parser.add_argument('-workers', '--workers', type=int, default=8, help='The number of parallel processes; the default is 8;')
	parser.add_argument('-window-size', '--window_size', type=int, default=10, help='The window size of skip-gram model; the default is 10;')
	parser.add_argument('-representation_size', '--representation_size', type=int, default=128, help='The number of latent dimensions to learn for each node; the default is 128')
	parser.add_argument('-p', '--p', type=float, default=1.0, help='p value')
	parser.add_argument('-q', '--q', type=float, default=1.0, help='q value')
	parser.add_argument('-alpha', '--alpha', type=float, default=1e-6, help='hyperparameter in SDNE that controls the first order proximity loss')
	parser.add_argument('-beta', '--beta', type=float, default=5, help='used for construct matrix B')
	parser.add_argument('-nu1', '--nu1', type=float, default=1e-5, help='controls l1-loss of weights in autoencoder')
	parser.add_argument('-nu2', '--nu2', type=float, default=1e-4, help='controls l2-loss of weights in autoencoder')
	parser.add_argument('-bs', '--bs', type=int, default=200, help='batch size')
	parser.add_argument('-lr', '--lr', type=float, default=0.01, help='learning rate')
	parser.add_argument('-alpha_verse', '--alpha_verse', type=float, default=0.85, help='alpha; default is 0.85')
	parser.add_argument('-lr_verse', '--lr_verse', type=float, default=0.0025, help='lr; default is 0.0025')
	parser.add_argument('-threads', '--threads', type=int, default=4, help='threads; default is 4')
	parser.add_argument('-nsamples', '--nsamples', type=int, default=3, help='nsamples; default is 3')
	args = parser.parse_args()

	cur_dir = os.path.abspath(getsourcefile(lambda:0))

	if args.community is None and not os.path.exists(args.edgelist.replace('edgelist','community')):
		cluster(args.edgelist,args.clustering)
		args.community = args.edgelist.replace('edgelist','community')

	alg_startTime = datetime.now()
	if args.algorithm == 'node2vec':
		os.system(f'python3 -m openne --method node2vec --input {args.edgelist} --graph-format edgelist --output result.embedding --number-walks {args.number_walks} --walk-length {args.walk_length} --workers {args.workers} --window-size {args.window_size} --representation-size {args.representation_size} --p {args.p} --q {args.q} >/dev/null 2>&1')
	elif args.algorithm == 'hope':
		os.system(f'python3 -m openne --method hope --input {args.edgelist} --graph-format edgelist --output result.embedding --representation-size {args.representation_size} >/dev/null 2>&1')
	elif args.algorithm == 'deepwalk':
		os.system(f'python3 -m openne --method deepWalk --input {args.edgelist} --graph-format edgelist --output result.embedding --number-walks {args.number_walks} --walk-length {args.walk_length} --workers {args.workers} --window-size {args.window_size} --representation-size {args.representation_size} >/dev/null 2>&1')
	elif args.algorithm == 'line':
		os.system(f'python3 -m openne --method line --input {args.edgelist} --graph-format edgelist --output result.embedding --representation-size {args.representation_size} >/dev/null 2>&1')
	elif args.algorithm == 'sdne':
		os.system(f'python3 -m openne --method sdne --input {args.edgelist} --graph-format edgelist --output result.embedding --encoder-list [128,{args.representation_size}] --alpha {args.alpha} --beta {args.beta} --nu1 {args.nu1} --nu2 {args.nu2} --bs {args.bs} --lr {args.lr} >/dev/null 2>&1')
	elif args.algorithm =='verse':
		if not os.path.exists(f'{args.edgelist.replace("edgelist","bcsr")}'):
			os.system(f'python3 {os.path.dirname(cur_dir)}/verse/python/convert.py --format edgelist {args.edgelist} {args.edgelist.replace("edgelist","bcsr")} >/dev/null 2>&1')
		os.system(f'{os.path.dirname(cur_dir)}/verse/src/verse -input {args.edgelist.replace("edgelist","bcsr")} -output result.embedding -dim {args.representation_size} -alpha {args.alpha_verse} -threads {args.threads} -nsamples {args.nsamples} -lr {args.lr_verse} >/dev/null 2>&1')
		g = buildGraph(args.edgelist, args.community)
		save_as_n2v(Embedding('result.embedding',args.representation_size).embeddings,'result.embedding',g['min'])
	alg_endTime = datetime.now()

	# with open(f'result.embedding', 'r') as fin:
	# 	data = fin.read().splitlines(True)
	# with open(f'result.embedding', 'w') as fout:
	# 	fout.writelines(data[1:])

	cge_path = cur_dir.replace('main.py','CGE/CGE_CLI.jl')
	results = ast.literal_eval(os.popen(f'julia {cge_path} -g {args.edgelist} -c {args.community} -e result.embedding -l {args.l} -f {args.f} -m {args.m}').read())
	
	print([results[1]]+[(alg_endTime - alg_startTime).total_seconds()])



