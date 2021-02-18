import os
import numpy as np

graph = "ABCD_Exp7.edgelist"
comm = "ABCD_Exp7.comm"
dims = [4, 8, 16, 32, 64, 128]
pth_samplers = "../../src/ABCD/utils"
verse_path = ".."

# Generate ABCD graph
os.system(f'julia {pth_samplers}/abcd_sampler.jl config_Exp7.toml')

# convert edgelist for Verse algorithm
os.system(
    f'python ../convert.py --format edgelist ABCD_Exp7.edgelist ABCD_Exp7.verse')

# create directory to store embeddings
if not os.path.exists("./embeddings"):
    os.makedirs("./embeddings")

# N2V
for dim in dims:
    os.system(
        f'python3 -m openne --method node2vec --input ./{graph} --graph-format edgelist --output ./embeddings/exp7_dim{dim}_node2vec.embedding --representation-size {dim}')
    print(f"N2V dim {dim} produced.")

for dim in dims:
    # DeepWalk
    os.system(
        f'python3 -m openne --method deepWalk --input ./{graph} --graph-format edgelist --output ./embeddings/exp7_dim{dim}_deepWalk.embedding --representation-size {dim}')
    print(f"DeepWalk dim {dim} produced.")

    # HOPE
    os.system(
        f'python3 -m openne --method hope --input ./{graph} --graph-format edgelist --output ./embeddings/exp7_dim{dim}_hope.embedding --representation-size {dim}')
    print(f"HOPE dim {dim} produced.")

    # SDNE
    os.system(
        f'python3 -m openne --method sdne --input ./{graph} --graph-format edgelist --output ./embeddings/exp7_dim{dim}_sdne.embedding --encoder-list [1000,{dim}]')
    print(f"SDNE dim {dim} produced.")

    # LINE
    os.system(
        f'python3 -m openne --method line --input ./{graph} --graph-format edgelist --output ./embeddings/exp7_dim{dim}_line.embedding --representation-size {dim}')
    print(f"LINE dim {dim} produced.")

    # VERSE
    os.system(
        f'{verse_path}/verse -input ABCD_Exp7.verse -output ./embeddings/exp7_dim{dim}_verse.embedding -dim {dim} -alpha 0.85 -threads 4 -nsamples 3')
    embeddings = np.fromfile(
        f"./embeddings/exp7_dim{dim}_verse.embedding", dtype=np.float32)
    embedding_shape = [int(embeddings.shape[0] / dim), dim]
    embeddings = embeddings.reshape(embedding_shape)
    np.savetxt(
        f'./embeddings/exp7_dim{dim}_verse.embedding', embeddings, delimiter=' ', fmt='%f')
    print(f"VERSE dim {dim} produced.")

# Preprocess files - UNIX systems
os.system('for f in embeddings/*; do sed 1d "$f" >tmpfile; mv tmpfile "$f"; done')
os.system(
    'for f in embeddings/*; do sort -k1,1 -n "$f" >tmpfile; mv tmpfile "$f"; done')
os.system(
    'for f in embeddings/*; do cut -d " " -f 2- "$f" >tmpfile; mv tmpfile "$f"; done')
os.system(f'cut -f 2 {comm} > {comm}.new && mv {comm}.new {comm}')
