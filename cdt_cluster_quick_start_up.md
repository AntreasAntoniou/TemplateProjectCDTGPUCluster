# GPU Cluster Quick-Start Guide

This guide is intended to guide students into the basics of using the charles GPU cluster. It is not intended to be
an exhaustive guide that goes deep into micro-details of the Slurm ecosystem. For an exhaustive guide please visit 
[the Slurm Documentation page.](https://slurm.schedmd.com/)

## What is the CDT GPU Cluster?
It's cluster consisting of server rack machines, each equipped with 4 GPUs of varying chipsets (mostly NVIDIA Titan X pascals, also NVIDIA Titan X and K40s). Currently there are about 52 GPUs available for use. The system is managed using the open source cluster management software named
 [Slurm](https://slurm.schedmd.com/overview.html). Slurm has various advantages over the competition, including full 
 support of GPU resource scheduling.
 
## Why do I need it?
Most Deep Learning experiments require a large amount of compute as you have noticed in term 1. Usage of GPU can 
accelerate experiments around 30-50x therefore making experiments that require a large amount of time feasible by 
slashing their runtimes down by a massive factor. For a simple example consider an experiment that required a month to 
run, that would make it infeasible to actually do research with. Now consider that experiment only requiring 1 day to 
run, which allows one to iterate over methodologies, tune hyperparameters and overall try far more things. This simple
example expresses one of the simplest reasons behind the GPU hype that surrounds machine learning research today.

## Getting Started

### Accessing the Cluster:
1. If you are not on a DICE machine, then ssh into your dice home using ```ssh sxxxxxx@student.ssh.inf.ed.ac.uk``` 
2. Then ssh into either mlp1 or mlp2 which are the headnodes of the GPU cluster - it does not matter which you use. To do that
 run ```ssh cdtcluster``` or ```ssh albert```.
3. You are now logged into the gpu cluster. If this is your first time logging in you'll need to build your environment.  This is because your home directory on the GPU cluster is separate to your usual AFS home directory on DICE.
- Note: Alternatively you can just ```ssh @sxxxxxxx@albert.inf.ed.ac.uk``` to get there in one step.

### Installing requirements:
1. Start by downloading the miniconda3 installation file using 
 ```wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh```.
2. Now run the installation using ```bash Miniconda3-latest-Linux-x86_64.sh```. At the first prompt reply yes. 
```
Do you accept the license terms? [yes|no]
[no] >>> yes
```
3. At the second prompt simply press enter.
```
Miniconda3 will now be installed into this location:
/home/sxxxxxxx/miniconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below
```
4. Now you need to activate your environment by first running:
```source .bashrc```.
This reloads .bashrc which includes the new miniconda path.
5. Run ```source activate``` to load miniconda root.
6. Now run ```conda create -n mlp python=3``` this will create the mlp environment. At the prompt choose y.
7. Now run ```source activate mlp```.
8. Install git using```conda install git```. Then config git using: 
```git config --global user.name "[your name]"; git config --global user.email "[matric-number]@sms.ed.ac.uk"```
9. Now clone the mlpractical repo using ```git clone https://github.com/CSTR-Edinburgh/mlpractical.git```.
10. Checkout the semester_2 branch using ```git checkout mlp2017-8/semester_2_materials```.
11. ```cd mlpractical``` and then install the required packages using ```pip install -r requirements_gpu.txt```.
12. This includes all of the required installations. Proceed to the next section outlining how to use the slurm cluster
 management software. Please remember to clean your setup files using ```conda clean -t```
 
### Using Slurm
Slurm provides us with some commands that can be used to submit, delete, view, explore current jobs, nodes and resources among others.
To submit a job one needs to use ```sbatch script.sh``` which will automatically find available nodes and pass the job,
 resources and restrictions required. The script.sh is the bash script containing the job that we want to run. Since we will be using the NVIDIA CUDA and CUDNN libraries 
 we have provided a sample script which should be used for your job submissions. The script is explained in detail below:
 
```bash
#!/bin/sh
#SBATCH -N 1	  # nodes requested
#SBATCH -n 1	  # tasks requested
#SBATCH --gres=gpu:1 # use 1 GPU
#SBATCH --mem=16000  # memory in Mb
#SBATCH -t 1:00:00  # time requested in hour:minute:seconds

# Setup CUDA and CUDNN related paths
export CUDA_HOME=/opt/cuda-8.0.44

export CUDNN_HOME=/opt/cuDNN-6.0_8.0

export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

# Setup a folder in the very fast scratch disk which can be used for storing experiment objects and any other files 
# that may require storage during execution.
mkdir -p /disk/scratch/${STUDENT_ID}

export TMPDIR=/disk/scratch/${STUDENT_ID}/
export TMP=/disk/scratch/${STUDENT_ID}/

# Activate the relevant virtual environment:

source /home/${STUDENT_ID}/miniconda3/bin/activate mlp

# Run the python script that will train our network
python network_trainer.py --batch_size 128 --epochs 200 --experiment_prefix vgg-net-emnist-sample-exp --dropout_rate 0.4 --batch_norm_use True --strided_dim_reduction True --seed 25012018

```

To actually run this use ```sbatch gpu_cluster_tutorial_training_script.sh```. When you do this, the job will be submitted and you will be given a job id.
```bash
[burly]sxxxxxxx: sbatch gpu_cluster_tutorial_training_script.sh 
Submitted batch job 147

```

To view a list of all running jobs use ```squeue``` for a minimal presentation and ```smap``` for a more involved presentation. Furthermore to view node information use ```sinfo```.
```bash
squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
               143 interacti     bash    iainr  R       8:00      1 landonia05
               147 interacti gpu_clus sxxxxxxx  R       1:05      1 landonia02

```
Also in case you want to stop/delete a job use ```scancel job_id``` where job_id is the id of the job.

Furthermore in case you want to test some of your code interactively to prototype your solution before you submit it to
 a node you can use ```srun -p interactive  --gres=gpu:2 --pty python my_code_exp.py```.

## Slurm Cheatsheet
For a nice list of most commonly used Slurm commands please visit [here](https://bitsanddragons.wordpress.com/2017/04/12/slurm-user-cheatsheet/).

## Syncing or copying data over to DICE

At some point you will need to copy your data to DICE so you can analyse them and produce charts, write reports, store for future use etc.
1. If you are on a terminal within I.F/A.T, then skip to step 2, if you are not, then, you'll first have to open a VPN into the university network using the instructions found [here](http://computing.help.inf.ed.ac.uk/openvpn).
2. From your local machine:
    1. To send data from a local machine to the cluster: ```rsync -ua --progress <local_path_of_data_to_transfer> <studentID>@albert.inf.ed.ac.uk:/home/<studentID>/path/to/folder```
    2. To receive data from the cluster to your local machine ```rsync -ua --progress <studentID>@albert.inf.ed.ac.uk:/home/<studentID>/path/to/folder <local_path_of_data_to_transfer> ```

## Additional Help

If you require additional help please post on the #gpu_cluster slack channel or if you are experiencing technical problems then please submit a computing support tickt.
