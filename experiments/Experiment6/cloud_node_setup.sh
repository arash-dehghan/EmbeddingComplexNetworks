#!/bin/bash
exec > /var/log/startuplog
exec 2>&1
echo "Starting setup"
apt-get update
echo "Installing NFS client"
apt install nfs-common -y
echo "Mount /home from login node"
sudo mount $IP:/home /home
echo "Install pip and upgrade it"
sudo apt install python3-pip -y
sudo -H pip3 install --upgrade pip
echo "Get Julia"
wget https://julialang-s3.julialang.org/bin/linux/x64/1.5/julia-1.5.3-linux-x86_64.tar.gz
tar zxvf julia-1.5.3-linux-x86_64.tar.gz
sudo mv julia-1.5.3 /usr/local
sudo ln -s /usr/local/julia-1.5.3/bin/julia /usr/bin/julia
echo "Install Python packages"
pip3 install pandas
pip3 install Pillow==8.0.1 scikit_learn==0.23.2 networkx==2.5 gensim==3.6.0 tensorflow==1.15.0 python_igraph==0.8.3 Click==7.0 click
echo "Install OpenNE"
cp -r /home/OpenNE ~
cd ~/OpenNE
sudo python3 setup.py install
echo "Add Julia packages"
julia -e 'using Pkg; Pkg.add(url="https://github.com/KrainskiL/CGE.jl")'
julia -e 'using Pkg; Pkg.add(url="https://github.com/bkamins/ABCDGraphGenerator.jl")'
cd /home/Experiment6
chmod +x /home/verse
python3 2_Exp6_Embeddings_divergence.py --sseed 25 --eseed 50