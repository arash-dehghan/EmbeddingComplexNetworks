import os
import subprocess
import ast
import numpy as np
from datetime import datetime
import time
import argparse
import random

exp = 3
tmp_emb = "/tmp/tmp.embedding"
ip = subprocess.check_output(
    "hostname -I", shell=True).decode()[:-2].replace(".", "")

parser = argparse.ArgumentParser(
    description=f'Run Experiment{exp} for given starting and ending seed.')
parser.add_argument('--sseed', type=int, help='Starting seed', required=True)
parser.add_argument('--eseed', type=int, help='Ending seed', required=True)
args = parser.parse_args()

dims = [32, 64, 128]
algs = ["node2vec", "deepWalk", "line", "sdne", "hope", "verse"]
graphs = os.listdir("graphs/networks")
graphs.sort()
graphs = graphs[args.sseed:args.eseed]

CGE_path= "../../src/CGE"
verse_path= ".."

if not os.path.exists("results"):
    os.makedirs("results")
    
for alg in algs:
    for dim in dims:
        ran = str(random.random()*10).replace(".", "")
        filename = f"Exp{exp}_dim{dim}_{alg}_{ip}_{ran}.csv"
        with open(f"results/{filename}", "w") as f:
            f.write('experiment,algorithm,beta,best_alpha,best_div_score,best_div_external,best_div_internal,dim,l,f,m,graph_seed,iter,alg_duration,cge_duration\n')
            for graph in graphs:
                alg_startTime = datetime.now()
                if alg == "verse":
                    os.system(f'{verse_path}/verse -input graphs/networks_verse/{graph} -output {tmp_emb} -dim {dim} -alpha 0.85 -threads 4 -nsamples 3 -lr 0.0025')
                    embeddings = np.fromfile(tmp_emb, dtype=np.float32)
                    embedding_shape = [int(embeddings.shape[0] / dim), dim]
                    embeddings = embeddings.reshape(embedding_shape)
                    np.savetxt(tmp_emb, embeddings,
                               delimiter=' ', fmt='%f')
                elif alg == "sdne":
                    os.system(
                        f'python3 -m openne --method sdne --input graphs/networks/{graph} --graph-format edgelist --output tmp.embedding --encoder-list [128,{dim}]')
                    os.system(f'sed -i 1d {tmp_emb};')
                else:
                    os.system(
                        f'python3 -m openne --method {alg} --input graphs/networks/{graph} --graph-format edgelist --output tmp.embedding --representation-size {dim}')
                    os.system(f'sed -i 1d {tmp_emb};')
                alg_endTime = datetime.now()
                comm = graph.replace("network", "community")
                cge_startTime = datetime.now()
                if alg == "verse":
                    results = os.popen(
                        f'julia {CGE_path}/CGE_CLI.jl -g graphs/networks/{graph} -c graphs/communities/{comm} -e tmp.embedding -l 200 -f 0 -m diameter -a').read()
                else:
                    results = os.popen(
                        f'julia {CGE_path}/CGE_CLI.jl -g graphs/networks/{graph} -c graphs/communities/{comm} -e tmp.embedding -l 200 -f 0 -m diameter').read()
                cge_endTime = datetime.now()
                data = ast.literal_eval(results)
                f.write(
                    f'{exp},{alg},{graph[-7:-4].replace("_",".")},{data[0]},{data[1]},{data[2]},{data[3]},{dim},200,0,diameter,{graph},{ip},{alg_endTime - alg_startTime},{cge_endTime - cge_startTime}\n')
