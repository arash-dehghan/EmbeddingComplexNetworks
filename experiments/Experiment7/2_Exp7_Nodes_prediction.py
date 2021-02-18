import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os
import ast

dims = [4, 8, 16, 32, 64, 128]
algs = ["deepWalk", "hope", "line", "node2vec", "sdne", "verse"]
CGE_path= "../../src/CGE"
graph = "ABCD_Exp7.edgelist"
comm = "ABCD_Exp7.comm"
exp = 7

y = pd.read_csv(comm, header=None)
for dim in dims:
    with open(f"Exp{exp}_dim{dim}.csv", "w") as f:
        f.write(
            'algorithm,dim,seed,acc,best_alpha,best_div_score,best_div_external,best_div_internal,l,f,m\n')
        for alg in algs:
            X = pd.read_csv(f"./embeddings/exp7_dim{dim}_{alg}.embedding",
                            header=None, delimiter=" ")
            # Calculate divergence
            results = os.popen(
                f'julia {CGE_path}/CGE_CLI.jl -g {graph} -c {comm} -e embeddings/exp7_dim{dim}_{alg}.embedding -l 200 -f 0 -m diameter -a').read()
            data = ast.literal_eval(results)
            for seed in range(10):
                # Split dataset with 75/25 ratio and fixed seed
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y.values.ravel(), test_size=0.25, random_state=seed)
                # Train XGBoost Classifier
                clf = xgb.XGBClassifier(
                    objective='multi:softmax', random_state=seed)
                clf.fit(X_train, y_train)
                acc = sum(y_test == clf.predict(X_test))/y_test.shape[0]
                f.write(
                    f'{alg},{dim},{seed},{acc},{data[0]},{data[1]},{data[2]},{data[3]},200,0,diameter\n')
                print(
                    f"Processed dim {dim}, alg {alg}, seed {seed}. Acc: {acc}, div: {data[1]}")
