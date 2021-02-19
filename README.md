This repository provides complementary code and data for the article [Evaluating Node Embeddings of Complex Networks](https://arxiv.org/abs/2102.08275).

### Repository structure
Repository groups files into 4 folders:
* `data` stores graphs and community files for 'real-world' graphs analyzed in the article
* `experiments` contains scripts used for conducted experiments, described in detail in the article
* `results` stores .csv files with experiments results - basis for graphs and analysis
* `src` directory include scripts, source files and packages utilized in the experiments

### Experiments mapping
We used numerical IDs for each experiment to simplify the scripts. Each ID correspond to following parameters/tasks:
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
Majority of the experiments was launched in distributed cloud environment and we provide Bash scripts used to set up computing nodes based on NFS storage. Please note that some scripts may perform correctly only on Unix-based systems, so we recommend using Linux distributions or macOS.
To prepare local environment for running the experiments following steps must be completed:
1. Install [Julia](https://julialang.org/downloads/) (experiments run under version 1.5.3)
2. Add required Julia packages
```bash
julia -e 'using Pkg; Pkg.add(url="https://github.com/KrainskiL/CGE.jl")'
julia -e 'using Pkg; Pkg.add(url="https://github.com/bkamins/ABCDGraphGenerator.jl")'
```
4. Install python dependencies from `requirements.txt`
```bash
pip -r requirements.txt
```
3. Install OpenNE package
```bash
cd src/OpenNE
python setup.py install
```
4. Compile [VERSE](https://github.com/xgfs/verse) executable for your system. `experiments` directory contain executable build for Ubuntu 18.04.

Each experiment's directory contains more details on specific execution procedure.

### Reproducibility
During computation randomnes was controlled with appropriate seeds, however embeddings for stochastic embedding algorithms may not be reproducible. Controlling output of embedding algorithms requires modifying OpenNE code. Additionaly, node2vec and DeepWalk use Worde2Vec embeddings as part of internal processing, which requires another mechanism of handling randomness. All other resources or computations are fully reproducible including:
* ABCD graphs and corresponding files for degree distribution, community sizes, etc.
* Train/test splits of graphs
* Output of classification models

### Acknowledgments
#### Computing environment
Experiments were conducted using [SOSCIP](https://www.soscip.org/) Cloud infrastructure based on OpenStack cloud system.
#### Embedding algorithms codebase
We used [OpenNE](https://github.com/thunlp/OpenNE) framework, that expose common interface to many embedding algorithms. For VERSE algorithm, implementation available under https://github.com/xgfs/verse was used.
