import argparse
import os
from inspect import getsourcefile

def one_to_zero_network(filename,newfilename):
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			l = line.split()
			l[0], l[1] = (int(l[0])-1),(int(l[1])-1)
			f = open(newfilename, "a")
			f.write(f"{l[0]} {l[1]}\n")

def one_to_zero_community(filename,newfilename):
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			l = line.split()
			l[1] = (int(l[1])-1)
			f = open(newfilename, "a")
			f.write(f"{l[1]}\n")


def create_community_sizes_file(n):
	percentages = [0.3,0.25,0.2,0.15,0.1]
	values = [int(p*n) for p in percentages]
	outF = open("community_sizes.txt", "w")
	for value in values:
	  outF.write(str(value))
	  outF.write("\n")
	outF.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='ABCD graph')
	parser.add_argument('-name', '--name', type=str, required = True)
	parser.add_argument('-n', '--n', type=int, help='number of vertices in graph', default = 10000)
	parser.add_argument('-t1', '--t1', type=float, default = 2.5, help='power-law exponent for degree distribution')
	parser.add_argument('-d_min', '--d_min', type=int, default=5, help='minimum degree')
	parser.add_argument('-d_max', '--d_max', type=int, default=50, help='maximum degree')
	parser.add_argument('-d_max_iter', '--d_max_iter', type=int, default=1000, help='maximum number of iterations for sampling degrees')
	parser.add_argument('-t2', '--t2', type=float, default=1.5, help='power-law exponent for cluster size distribution')
	parser.add_argument('-c_min', '--c_min', type=int, default=50, help='minimum cluster size')
	parser.add_argument('-c_max', '--c_max', type=int, default=1000, help='maximum cluster size')
	parser.add_argument('-c_max_iter', '--c_max_iter', type=int, default=1000, help='maximum number of iterations for sampling cluster sizes')
	parser.add_argument('-xi', '--xi', type=float, default=0.2, help='fraction of edges to fall in background graph')
	parser.add_argument('-isCL', '--isCL', type=str, choices=['true', 'false'], default="false", help='Maximum size of communities in the graph. If not specified, this is set to n, the total number of nodes in the graph.')
	parser.add_argument('-islocal', '--islocal', type=str, choices=['true', 'false'],  default="false", help='islocal')
	parser.add_argument('-degreefile', '--degreefile', type=str, default=None, help='name of file to generate that contains vertex degrees')
	parser.add_argument('-communitysizesfile', '--communitysizesfile', type=str, default=None, help='name of file to generate that contains community sizes')
	parser.add_argument('-communityfile', '--communityfile', type=str, default='network.community', help='name of file to generate that contains assignments of vertices to communities')
	parser.add_argument('-networkfile', '--networkfile', type=str, default='network.edgelist', help='name of file to generate that contains edges of the generated graph')
	parser.add_argument('-seed', '--seed', type=int, default=1, help='seed')
	parser.add_argument('-xiormu', '--xiormu', type=str, choices=['xi', 'mu'], default='xi', help='name of file to generate that contains edges of the generated graph')
	args = parser.parse_args()

	path = os.path.abspath(getsourcefile(lambda:0)).replace('ABCD.py','utils')
	data_path = f'{path[:-15]}/data'

	if args.degreefile is None:
		os.system(f'julia {path}/deg_sampler.jl degrees.txt {args.t1} {args.d_min} {args.d_max} {args.n} {args.d_max_iter} {args.seed}')
		args.degreefile = 'degrees.txt'

	if args.communitysizesfile is None:
		os.system(f'julia {path}/com_sampler.jl community_sizes.txt {args.t2} {args.c_min} {args.c_max} {args.n} {args.c_max_iter} {args.seed}')
		args.communitysizesfile = 'community_sizes.txt'

	if args.communitysizesfile == "generate":
		create_community_sizes_file(args.n)
		args.communitysizesfile = 'community_sizes.txt'

	os.system(f'julia {path}/graph_sampler.jl {args.networkfile} {args.communityfile} {args.degreefile} {args.communitysizesfile} {args.xiormu} {args.xi} {args.isCL} {args.islocal} {args.seed}')

	if not os.path.isdir(f"{data_path}/{args.name}"):
		os.makedirs(f'{data_path}/{args.name}')

	one_to_zero_network(args.networkfile,f'{data_path}/{args.name}/{args.name}.edgelist')
	one_to_zero_community(args.communityfile,f'{data_path}/{args.name}/{args.name}.community')

	for file in [args.communityfile, args.networkfile]:
		os.remove(file)
