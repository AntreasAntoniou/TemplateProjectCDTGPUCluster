#!/bin/sh

cd ..
export DATASET_DIR="data/"
# Activate the relevant virtual environment:

python $execution_script$ --filepath_to_arguments_json_file experiment_config_files/$experiment_config$