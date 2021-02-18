import os

seed = 1
pth_samplers ="../../src/ABCD/utils"
pth_comm_sizes = "../community_sizes.txt"
exp = 11
comm=f'exp{exp}_seed{seed}.comm'
graph = f'exp{exp}_seed{seed}.edgelist'

if not os.path.exists("graphs"):
    os.makedirs("graphs")

degrees_name = f"exp{exp}_seed{seed}.degrees"
os.system(f'julia {pth_samplers}/deg_sampler.jl graphs/{degrees_name} 2.5 5 464 10000 1000 {seed}')
# [ Info: Usage: julia deg_sampler.jl filename τ₁ d_min d_max n max_iter [seed]
# [ Info: Example: julia deg_sampler.jl degrees.dat 3 5 50 10000 1000 42

os.system(f'julia {pth_samplers}/graph_sampler.jl graphs/{graph} graphs/{comm} graphs/{degrees_name} {pth_comm_sizes} xi 0.2 false false {seed}')
# [ Info: Usage: julia graph_sampler.jl networkfile communityfile degreefile communitysizesfile mu|xi fraction isCL islocal [seed]
# [ Info: Example: julia graph_sampler.jl network.dat community.dat degrees.dat community_sizes.dat xi 0.2 true false 42

# removing first column (vertices id) from communities file - only UNIX systems
os.system(f'cut -f 2 graphs/{comm} > graphs/{comm}.new && mv graphs/{comm}.new graphs/{comm};')

# convert edgelists for Verse algorithm
os.system(f'python ../convert.py --format graphs/{graph} graphs/{graph}.verse')