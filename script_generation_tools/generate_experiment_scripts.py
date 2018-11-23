import os
import sys
from copy import copy
import argparse

experiment_json_dir = '../experiment_config_files/'
maml_experiment_script = 'train_evaluate_emnist_classification_system.py'
cluster_scripts = {"gpu_cluster": "cluster_template_script", "remote_machine": "remote_machine_script"}
local_script_dir = "../experiment_scripts"
cluster_script_dir = "../cluster_experiment_scripts"

if not os.path.exists(local_script_dir):
    os.makedirs(local_script_dir)

if not os.path.exists(cluster_script_dir):
    os.makedirs(cluster_script_dir)

def load_template(filepath):
    with open(filepath, mode='r') as filereader:
        template = filereader.readlines()

    return template

def fill_template(template_list, execution_script, experiment_config):
    template_list = copy(template_list)
    execution_line = template_list[-1]
    execution_line = execution_line.replace('$execution_script$', execution_script)
    execution_line = execution_line.replace('$experiment_config$', experiment_config)
    template_list[-1] = execution_line
    script_text = ''.join(template_list)

    return script_text

def write_text_to_file(text, filepath):
    with open(filepath, mode='w') as filewrite:
        filewrite.write(text)


local_script_template = load_template('local_run_template_script.sh')

for subdir, dir, files in os.walk(experiment_json_dir):
    for file in files:
        if file.endswith('.json'):
            config = file

            experiment_script = maml_experiment_script

            for name, cluster_script_template_f in cluster_scripts.items():
                cluster_script_template = load_template('{}.sh'.format(cluster_script_template_f))
                cluster_script_text = fill_template(template_list=cluster_script_template,
                                                    execution_script=experiment_script,
                                                    experiment_config=file)
                cluster_script_name = '{}/{}_{}.sh'.format(cluster_script_dir, file.replace(".json", ''), name)
                cluster_script_name = os.path.abspath(cluster_script_name)

                write_text_to_file(cluster_script_text, filepath=cluster_script_name)

            local_script_text = fill_template(template_list=local_script_template,
                                                execution_script=experiment_script,
                                                experiment_config=file)

            local_script_name = '{}/{}.sh'.format(local_script_dir, file.replace(".json", ''))
            local_script_name = os.path.abspath(local_script_name)
            write_text_to_file(text=local_script_text, filepath=local_script_name)
