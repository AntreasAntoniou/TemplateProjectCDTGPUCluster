# CDT Cluster Template Project
A short code repo that showcases a potential framework for carrying out experiments on the CDT Cluster.

## Installation

The code uses Pytorch to run, along with many other smaller packages. To take care of everything at once, we recommend 
using the conda package management library. More specifically, 
[miniconda3](https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh), as it is lightweight and fast to install.
If you have an existing miniconda3 installation please start at step 3. 
If you want to  install both conda and the required packages, please run:
 1. ```wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh```
 2. Go through the installation.
 3. Activate conda
 4. conda create -n mlp python=3.6.
 5. conda activate mlp
 6. At this stage you need to choose which version of pytorch you need by visiting [here](https://pytorch.org/get-started/locally/)
 7. Choose and install the pytorch variant of your choice using the conda commands.
 8. Then run ```bash install.sh```

To execute an installation script simply run:
```bash <installation_file_name>```

To activate your conda installations simply run:
```conda activate```

## Overview of code:

- [cluster_experiment_scripts](cluster_experiment_scripts/): Contains automatically generated experiment scripts, 
ready to be submitted to slurm, along with "hurdle-reducing" scripts, that automate job submission, provide job progress/performance tracking, ensure jobs keep running, and allow choice over the number of parallel jobs one wants to have running in the cluster at any given time.
- [cluster_experiment_scripts/run_jobs_simple.py](cluster_experiment_scripts/run_jobs_simple.py): A python script that automates job submission and provides functionality for constraining the total number of jobs submitted to the cluster at any given time. It also ensures jobs keep running, by periodically checking the queue, and resubmitting a job if it can not be found in the queue.
- [cluster_experiment_scripts/run_jobs_with_real_time_metrics.py](cluster_experiment_scripts/run_jobs_with_real_time_metrics.py): A more advanced variant of the above script. In addition to the "simple" script's functionality, it also keeps track of the progress of each experiment, and can present current performance statistics in real time.
- [data](data/): Contains the EMNIST dataset, which will be used by the sample experiment framework.
- [experiment_config_template_files](experiment_config_template_files): Contains json template config files with some variable
 hyperparameters (indicated by $<hyper-parameter name>$). These json files will be used by the script generation tools
 to automatically generate your experiment configs and experiment scripts.
- [experiment_config_files](experiment_config_files): Contains the automatically generated experiment config files.
- [script_generation_tools](script_generation_tools): Contains an array of experiment script generation tools. More specifically:
    - [generate_configs.py](script_generation_tools/generate_configs.py): Generates experiment configuration files given
     a configuration template and a number of experiment hyper-parameter settings.
    - [generate_experiment_scripts.py](script_generation_tools/generate_experiment_scripts.py): Uses the automatically 
    generated config files along with the template experiment bash scripts contained in the same folder to generate experiment scripts ready to be run locally, on the cluster or on GPU boxes often found in research groups.
    - [cluster_template_script.sh](script_generation_tools/cluster_template_script.sh): A template bash script that runs an experiment on the CDT Cluster.
    - [local_run_template_script.sh](script_generation_tools/local_run_template_script.sh): A template bash script that runs an experiment on a local machine.
    - [gpu_box_experiment_template_script.sh](script_generation_tools/gpu_box_experiment_template_script.sh): A template bash script for running experiments on a GPU box machine.
- [arg_extractor.py](arg_extractor.py): Contains an array of utility methods that can parse python arguments or convert
 a json config file into an argument NamedTuple.
- [data_providers.py](data_providers.py): A sample data provider, of the same type used in the MLPractical course.
- [experiment_builder.py](experiment_builder.py): Builds and executes a simple image classification experiment, keeping track
of relevant statistics, taking care of storing and re-loading pytorch models, as well as choosing the best validation-performing model to evaluate the test set on.
- [model_architectures.py](model_architectures.py): Provides a fully connected network and convolutional neural network 
sample models, which have a number of moving parts indicated as hyperparameters.
- [storage_utils.py](storage_utils.py): Provides a number of storage/loading methods for the experiment statistics.
- [train_evaluated_emnist_classification_system.py](train_evaluate_emnist_classification_system.py): Runs an experiment 
given a data provider, an experiment builder instance and a model architecture
# Running an experiment
To run a default image classification experiment using the template models I provided:
1. Sign into the cluster using ssh sxxxxxxx@albert.inf.ed.ac.uk
2. Activate your conda environment using, source miniconda3/bin/activate ; conda activate mlp
3. cd TemplateProjectCDTGPUCluster
4. cd cluster_experiment_scripts
5. Find which experiment(s) you want to run (make sure the experiment ends in 'gpu_cluster.sh'). Decide if you want to run a single experiment or multiple experiments in parallel.
    1. For a single experiment: ``sbatch experiment_script.sh```
    2. To run multiple experiments using the "hurdle-reducing" script that automatically submits jobs, makes sure the jobs are always running, keeps track of progress and even provides a glimpse into the current performance of the system in real time:
        1. Make sure the cluster_experiment_scripts folder contains ***only*** the jobs you want to run. 
        2. Run the command: ```python run_jobs_with_real_time_metrics.py --num_parallel_jobs <number of jobs to keep in the slurm queue at all times> --num_epochs <number of epochs to run each job>```
        
To run a custom/new experiment on any dataset:
1. Sign into the cluster using ssh sxxxxxxx@albert.inf.ed.ac.uk
2. Activate your conda environment using, source miniconda3/bin/activate ; conda activate mlp
3. cd TemplateProjectCDTGPUCluster
1. Modify the existing codebase or replace with your own pytorch code, making sure that each script can automatically find where it left off on its own if it's killed for any reason.
2. Write a config template that includes all the arguments your experiment will require, for any hyper-parameters you want to vary over different experiment types use a $variable_name$ value, which will be replaced by the automated script generator.
3. Place the template script in [experiment_config_template_files](experiment_config_template_files/)
4. For example let's have a look at the sample template script that this repo comes with:
```json
{
  "batch_size": 100,
  "continue_from_epoch": -1,
  "seed": $seed$,
  "image_num_channels": 1,
  "image_height": 28,
  "image_width": 28,
  "dim_reduction_type": "$dim_reduction_type$",
  "num_layers": $num_layers$,
  "num_filters": $num_filters$,
  "num_epochs": $num_epochs$,
  "experiment_name": "$experiment_name$",
  "use_gpu": true,
  "gpu_id": "0",
  "weight_decay_coefficient": 1e-05
}
```
5. One can easily see that some variables use the $<variable_name>$ syntax, to indicate that they are hyper-parameters that the automatic config generation tools can change.
6. Once a template script is ready, open the [generate_configs.py](script_generation_tools/generate_configs.py) under script_generation_tools.
7. Inside the script one can find a list of config NamedTuples. The definition of a config file can be changed to include all the hyperparameters you want to include by adding or removing variable name arguments from the NamedTuple initialization line. 
Each one of those indicates an experiment the user wants to run. Their generation can be automated using standard programming structures (i.e. loops, dictionaries, list comprehensions, classes etc.). Create all the desired experiment config NamedTuples by any method you'd like.
8. ```cd script_generation tools```
9. ```python generate_configs.py; python generate_scripts.py```
10. Your new cluster scripts can be found in the cluster_experiment_scripts, ready to be run.
11. cd cluster_experiment_scripts
12. Find which experiment(s) you want to run (make sure the experiment ends in 'gpu_cluster.sh'). Decide if you want to run a single experiment or multiple experiments in parallel.
    1. For a single experiment: ``sbatch experiment_script.sh```
    2. To run multiple experiments using the "hurdle-reducing" script that automatically submits jobs, makes sure the jobs are always running, keeps track of progress and even provides a glimpse into the current performance of the system in real time:
        1. Make sure the cluster_experiment_scripts folder contains ***only*** the jobs you want to run. 
        2. Run the command: ```python run_jobs_with_real_time_metrics.py --num_parallel_jobs <number of jobs to keep in the slurm queue at all times> --num_epochs <number of epochs to run each job>```
         

 
