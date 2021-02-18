import os

# Betas
parameters = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
seeds = range(10)
pth_samplers = "../../src/ABCD/utils"
pth_degrees = "degrees.txt"
exp = 3

# create directories to store produced files
if not os.path.exists("graphs/comm_sizes"):
    os.makedirs("graphs/comm_sizes")
if not os.path.exists("graphs/networks"):
    os.makedirs("graphs/networks")
if not os.path.exists("graphs/communities"):
    os.makedirs("graphs/communities")
if not os.path.exists("graphs/networks_verse"):
    os.makedirs("graphs/networks_verse")

# loop through betas and seeds to create 100 graphs
for param in parameters:
    for seed in seeds:
        seed = seed + 10*parameters.index(param)
        param_file = str(param).replace(".", "_")
        sizes_name = f"graphs/comm_sizes/exp{exp}_comm_sizes_seed{seed}_param{param_file}.dat"
        os.system(
            f'julia {pth_samplers}/com_sampler.jl {sizes_name} {param} 50 1000 10000 1000 {seed}')
        # [ Info: Usage: julia com_sampler.jl filename τ₂ c_min c_max n max_iter [seed]
        # [ Info: Example: julia com_sampler.jl community_sizes.dat 2 50 1000 10000 1000 42
        os.system(f'julia {pth_samplers}/graph_sampler.jl graphs/networks/exp{exp}_network_seed{seed}_param{param_file}.dat' +
                  f'graphs/communities/exp{exp}_community_seed{seed}_param{param_file}.dat' + 
                  f'{pth_degrees} {sizes_name} xi 0.2 false false {seed}')
        # [ Info: Usage: julia graph_sampler.jl networkfile communityfile degreefile communitysizesfile mu|xi fraction isCL islocal [seed]
        # [ Info: Example: julia graph_sampler.jl network.dat community.dat degrees.dat community_sizes.dat xi 0.2 true false 42
# removing first column (vertices id) from communities files - only UNIX systems
os.system('for f in graphs/communities/*; do cut -f 2 "$f" > "$f".new && mv "$f".new "$f"; done')

# convert edgelists for Verse algorithm
for network in os.listdir('graphs/networks'):
    os.system(
        f'python ../convert.py --format edgelist graphs/networks/{network} graphs/networks_verse/{network}')
