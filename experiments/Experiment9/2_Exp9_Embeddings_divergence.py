import os
import subprocess
import ast
import numpy as np
from datetime import datetime
import time
import random

exp = 9
tmp_emb = "/tmp/tmp.embedding"
ip = subprocess.check_output("hostname -I",shell=True).decode()[:-2].replace(".","")

dims = [4, 8, 16, 32, 64, 128]
algs = ["node2vec","deepWalk","line","sdne","hope","verse"]
graphs = os.listdir("graphs/networks")
CGE_path= "../../src/CGE"

if not os.path.exists("results"):
    os.makedirs("results")

for alg in algs:
    ran = str(random.random()*10).replace(".","")
    filename = f"Exp{exp}_{alg}_{ip}_{ran}.csv"
    with open(f"results/{filename}","w") as f:
        f.write('experiment,algorithm,best_alpha,best_div_score,best_div_external,best_div_internal,dim,l,f,m,graph,iter,alg_duration,cge_duration\n')
        for dim in dims:
            for graph in graphs:
                alg_startTime = datetime.now()
                if alg == "verse":
                    os.system(f'./verse -input graphs/networks_verse/{graph} -output {tmp_emb} -dim {dim} -alpha 0.85 -threads 8 -nsamples 3 -lr 0.0025')
                    embeddings = np.fromfile(tmp_emb, dtype=np.float32)
                    embedding_shape = [int(embeddings.shape[0] / dim), dim]
                    embeddings = embeddings.reshape(embedding_shape)
                    np.savetxt(tmp_emb, embeddings, delimiter=' ', fmt='%f')
                elif alg == "sdne":
                    os.system(f'python3 -m openne --method sdne --input graphs/networks/{graph} --graph-format edgelist --output {tmp_emb} --encoder-list [128,{dim}]')
                    os.system(f'sed -i 1d {tmp_emb};')
                else:
                    os.system(f'python3 -m openne --method {alg} --input graphs/networks/{graph} --graph-format edgelist --output {tmp_emb} --representation-size {dim}')
                    os.system(f'sed -i 1d {tmp_emb};')
                alg_endTime = datetime.now()
                comm = graph.replace("edgelist","ecg")
                cge_startTime = datetime.now()
                if alg == "verse":
                    results = os.popen(f'julia {CGE_path}/CGE_CLI.jl -g graphs/networks/{graph} -c graphs/communities/{comm} -e {tmp_emb} -l 200 -f 0 -m diameter -a').read()
                else:
                    results = os.popen(f'julia {CGE_path}/CGE_CLI.jl -g graphs/networks/{graph} -c graphs/communities/{comm} -e {tmp_emb} -l 200 -f 0 -m diameter').read()
                cge_endTime = datetime.now()
                data = ast.literal_eval(results)
                f.write(f'{exp},{alg},{data[0]},{data[1]},{data[2]},{data[3]},{dim},200,0,diameter,{graph},{ip},{alg_endTime - alg_startTime},{cge_endTime - cge_startTime}\n')
