import os

# Deltas_exponent
parameters = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
seeds = range(10)
pth_samplers = "../../src/ABCD/utils"
pth_comm_sizes = "../community_sizes.txt"
exp = 8

# create directories to store produced files
if not os.path.exists("./graphs/degrees"):
    os.makedirs("./graphs/degrees")
if not os.path.exists("./graphs/networks"):
    os.makedirs("./graphs/networks")
if not os.path.exists("./graphs/communities"):
    os.makedirs("./graphs/communities")
if not os.path.exists("./graphs/networks_verse"):
    os.makedirs("./graphs/networks_verse")

for param in parameters:
    for seed in seeds:
        seed = seed + 10*parameters.index(param)
        param_file = str(param).replace(".", "_")
        degrees_name = f"graphs/degrees/exp{exp}_degree_seed{seed}_param{param_file}.dat"
        os.system(
            f'julia {pth_samplers}/deg_sampler.jl {degrees_name} 2.5 5 {int(10000**param)} 10000 1000 {seed}')
        # [ Info: Usage: julia deg_sampler.jl filename τ₁ d_min d_max n max_iter [seed]
        # [ Info: Example: julia deg_sampler.jl degrees.dat 3 5 50 10000 1000 42
        os.system(f'julia {pth_samplers}/graph_sampler.jl graphs/networks/exp{exp}_network_seed{seed}_param{param_file}.dat graphs/communities/exp{exp}_community_seed{seed}_param{param_file}.dat {degrees_name} {pth_comm_sizes} xi 0.2 false false {seed}')
        # [ Info: Usage: julia graph_sampler.jl networkfile communityfile degreefile communitysizesfile mu|xi fraction isCL islocal [seed]
        # [ Info: Example: julia graph_sampler.jl network.dat community.dat degrees.dat community_sizes.dat xi 0.2 true false 42
# removing first column (vertices id) from communities files - only UNIX systems
os.system('for f in graphs/communities/*; do cut -f 2 "$f" > "$f".new && mv "$f".new "$f"; done')

# convert edgelists for Verse algorithm
for network in os.listdir('graphs/networks'):
    os.system(
        f'python ../convert.py --format edgelist graphs/networks/{network} graphs/networks_verse/{network}')
