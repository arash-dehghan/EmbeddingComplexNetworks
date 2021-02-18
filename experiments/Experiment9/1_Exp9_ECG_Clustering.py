import networkx as nx
import igraph as ig
import pandas as pd
import numpy as np
import partition_igraph
import argparse
import os


def ecg(filename, commfile):
    with open(filename, 'r') as f:
        edges = [tuple(map(int, i.split(' '))) for i in f]
    g = ig.Graph.TupleList(edges)

    idx = np.argsort(g.vs['name'])

    m = g.community_ecg(min_weight=.5).membership
    ec = [m[i] for i in idx]  # re-ordering to follow node order from the file
    with open(commfile, 'w') as f:
        f.write('\n'.join(str(x) for x in ec))


def louvain(filename, commfile):
    with open(filename, 'r') as f:
        edges = [tuple(map(int, i.split(' '))) for i in f]
    g = ig.Graph.TupleList(edges)

    idx = np.argsort(g.vs['name'])

    m = g.community_multilevel().membership
    ml = [m[i] for i in idx]  # re-ordering to follow node order from the file
    with open(commfile, 'w') as f:
        f.write('\n'.join(str(x) for x in ml))


datapath = "../../data"
graphs = ["airports", "emaileu", "github", "mousebrain"]
for graph in graphs:
    print("Processing "+graph+" graph")
    ecg(datapath+graph+".edgelist", graph+".community")
    # prepare networks for VERSE algorithm
    os.system(
        f'python ../convert.py --format edgelist {datapath+graph}.edgelist {graph}.edgelist')
