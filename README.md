This repository provides complementary code and data for the article [Evaluating Node Embeddings of Complex Networks](https://arxiv.org/abs/2102.08275).

### Repository structure
Repository groups files into 4 folders:
* `data` stores graphs and community files used in the experiments
* `experiments` contains scripts for conducting experiments, script with utility functions and data used to produce specific graphs
* `results` stores .csv files with results of experiments
* `src` directory include external scripts, source files and packages utilized in the experiments

### Experiments mapping
We used numerical IDs for each experiment to simplify notation in the scripts. Each ID correspond to following tasks:
|Experiment ID | Description |
|--------------|-------------|
|1|Divergence and variance on one ABCD graph with default parameters|
|2|Sensitivity analysis for &xi;|
|3|Sensitivity analysis for &beta;|
|4|Sensitivity analysis for &gamma;|
|5|Sensitivity analysis for node2vec _p_ and _q_ parameters;|
|6|Sensitivity analysis for _n_|
|7|Nodes Classification|
|8|Sensitivity analysis for &Delta;|
|9|Divergence and variance for Mousebrain, Airports, GitHub and EmailEU graphs|
|10|Community Detection|
|11|Link Prediction|

### Execution in local environment
Majority of the experiments were launched in cloud environment due to high computational requirements.
To prepare local environment for the experiments please follow guidelines below:
1. Install [Julia](https://julialang.org/downloads/) (experiments ran using Julia 1.5.3)
2. Add required Julia packages
```bash
julia -e 'using Pkg; Pkg.add(url="https://github.com/KrainskiL/CGE.jl")'
julia -e 'using Pkg; Pkg.add(url="https://github.com/bkamins/ABCDGraphGenerator.jl")'
```
4. Install python dependencies from `requirements.txt`
```bash
pip -r requirements.txt
```
3. Download and install [OpenNE](https://github.com/thunlp/OpenNE) package
```bash
git clone https://github.com/thunlp/OpenNE.git
cd src
python setup.py install
```
4. Download and compile [VERSE](https://github.com/xgfs/verse) executable for your OS. `src/verse/src` directory contain executable build for Ubuntu 18.04. For more details please check VERSE repository.
```bash
git clone https://github.com/xgfs/verse.git
cd src && make;
```

Each experiment can be conducted by runnin `experiment.py` in appropriate folder in `experiments` directory.

### Reproducibility
Presented experiments include multiple random processes, in particular:
* generation of synthetic ABCD graphs
* generation of embeddings (excluding deterministic HOPE and LINE)
* splitting data to train and test subsets
* training of classification models (XGBoost)

All abovementioned algorithms were controlled with proper seeding excluding generation of embedding which would require modification to OpenNE package and additional constraints for specific embedding algorithms (Node2Vec and DeepWalk rely on external Word2Vec implementation different seeding mechanism). As embedding algorithms provide minor contribution to the overall variance of output measures, executing experiments in current setup should still produce results closely resembling the original ones.

### Acknowledgments
#### Computing environment
Experiments were conducted using [SOSCIP](https://www.soscip.org/) Cloud infrastructure based on OpenStack cloud system.
#### Embedding algorithms codebase
We used [OpenNE](https://github.com/thunlp/OpenNE) framework, that expose common interface to many embedding algorithms. For VERSE algorithm, implementation available under https://github.com/xgfs/verse was used.
