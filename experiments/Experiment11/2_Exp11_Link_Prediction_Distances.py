import igraph as ig
import os
import subprocess
from sklearn.metrics import roc_auc_score, accuracy_score
import numpy as np
import pandas as pd
import argparse
import ast
import random

exp = 11
ip = subprocess.check_output(
    "hostname -I", shell=True).decode()[:-2].replace(".", "")
parser = argparse.ArgumentParser(
    description=f'Run Experiment{exp} for given random seed.')
parser.add_argument('--seed', type=int, help='Random seed', required=True)
args = parser.parse_args()

datadir = "graphs/networks_red/"
dims = [4, 8, 16, 32, 64, 128]
algs = ["node2vec", "deepWalk", "line", "sdne", "hope", "verse"]
tmp_emb = "/tmp/tmp.embedding"
graph = "exp11_seed1.edgelist"
seed = args.seed

# create directories to store embeddings and reduced graphs
if not os.path.exists("./embeddings"):
    os.makedirs("./embeddings")
if not os.path.exists("./graphs/networks_red"):
    os.makedirs("./graphs/networks_red")

G = ig.Graph.Read_Ncol("exp11_seed1.edgelist" + graph, directed=False)
test_size = int(np.round(.1*G.ecount()))

CGE_path = "../../src/CGE"
verse_path = ".."
if not os.path.exists("results"):
    os.makedirs("results")

for seed in range(10):
    np.random.seed(seed)
    test_eid = np.random.choice(G.ecount(), size=test_size, replace=False)
    edges = [(G.es[eid].source, G.es[eid].target) for eid in test_eid]
    with open(f"graphs/networks_red/exp11_seed{seed}_removed.edgelist", "w") as f:
        for vid in edges:
            f.write(str(vid[0])+" "+str(vid[1])+"\n")
    Gp = G.copy()
    Gp.delete_edges(test_eid)
    reduced_graph = f"graphs/networks_red/exp11_seed{seed}_reduced.edgelist"
    Gp.write(reduced_graph, format="edgelist")
    reduced_verse = reduced_graph+".verse"
    os.system(
        f'python3 ../convert.py --format edgelist {reduced_graph} {reduced_verse}')

    for alg in algs:
        filename = f"Exp{exp}_alg{alg}_results_{ip}_seed{seed}.csv"
        with open(f"results/{filename}", "w") as res:
            res.write(
                'experiment,algorithm,auc,acc,best_alpha,best_div_score,best_div_external,best_div_internal,l,f,m,dim,graph,seed\n')
            for dim in dims:
                if alg == "verse":
                    os.system(
                        f'{verse_path}/verse -input {reduced_verse} -output {tmp_emb} -dim {dim} -alpha 0.85 -threads 4 -nsamples 3 -lr 0.0025')
                    embeddings = np.fromfile(tmp_emb, dtype=np.float32)
                    embedding_shape = [int(embeddings.shape[0] / dim), dim]
                    embeddings = embeddings.reshape(embedding_shape)
                    np.savetxt(tmp_emb, embeddings, delimiter=' ', fmt='%f')
                elif alg == "sdne":
                    os.system(
                        f'python3 -m openne --method sdne --input {reduced_graph} --graph-format edgelist --output {tmp_emb} --encoder-list [128,{dim}]')
                    os.system(f'sed -i 1d {tmp_emb};')
                else:
                    os.system(
                        f'python3 -m openne --method {alg} --input {reduced_graph} --graph-format edgelist --output {tmp_emb} --representation-size {dim}')
                    os.system(f'sed -i 1d {tmp_emb};')
                # features for node pairs without edges
                ctr = 0
                counter = 0
                nonedges = []
                while ctr < len(edges):
                    np.random.seed(seed+counter+1)
                    e = np.random.choice(G.vcount(), size=2, replace=False)
                    if G.get_eid(e[0], e[1], directed=False, error=False) == -1:
                        nonedges.append((e[0], e[1]))
                        ctr += 1
                    counter += 1
                X = pd.read_csv(tmp_emb, sep=' ', header=None)
                if alg != "verse":
                    X = X.sort_values(by=0)
                    X = np.array(X.iloc[:, 1:])
                else:
                    X = np.array(X)
                edges_dist = [np.linalg.norm(X[e[0]]-X[e[1]]) for e in edges]
                nonedges_dist = [np.linalg.norm(
                    X[e[0]]-X[e[1]]) for e in nonedges]
                true_y = [1]*len(edges)+[0]*len(nonedges)
                score = np.array(edges_dist+nonedges_dist)
                score = 1-score/np.max(score)
                roc = roc_auc_score(true_y, score)
                acc = accuracy_score(true_y, score > np.median(score))
                if alg == "verse":
                    results = os.popen(
                        f'julia {CGE_path}/CGE_CLI.jl -g {reduced_graph} -c graphs/exp11_seed1.comm -e {tmp_emb} -l 200 -f 0 -m diameter -a').read()
                else:
                    results = os.popen(
                        f'julia {CGE_path}/CGE_CLI.jl -g {reduced_graph} -c graphs/exp11_seed1.comm -e {tmp_emb} -l 200 -f 0 -m diameter').read()
                data = ast.literal_eval(results)
                res.write(
                    f'{exp},{alg},{roc},{acc},{data[0]},{data[1]},{data[2]},{data[3]},200,0,diameter,{dim},exp11_seed1.comm,{seed}\n')
