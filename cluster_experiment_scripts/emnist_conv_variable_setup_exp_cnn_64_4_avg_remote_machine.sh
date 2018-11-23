#!/bin/sh
export CUDA_HOME=/opt/cuda-9.0.176.1/

export CUDNN_HOME=/opt/cuDNN-7.0/

export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

cd ..
export DATASET_DIR="datasets/"
# Activate the relevant virtual environment:

python train_evaluate_emnist_classification_system.py --filepath_to_arguments_json_file experiment_config_files/emnist_conv_variable_setup_exp_cnn_64_4_avg.json