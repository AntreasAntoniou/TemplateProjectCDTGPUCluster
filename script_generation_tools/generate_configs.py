import os
from collections import namedtuple

config = namedtuple('config', 'experiment_name num_epochs '
                              'num_filters '
                              'num_layers '
                              'dim_reduction_type, seed')

experiment_templates_json_dir = '../experiment_config_template_files/'
experiment_config_target_json_dir = '../experiment_config_files/'

configs_list = [config(experiment_name='exp_cnn_32_4_avg', num_epochs=15, num_filters=32, num_layers=4,
                       dim_reduction_type='avg_pooling', seed=0),
                config(experiment_name='exp_cnn_64_4_avg', num_epochs=10, num_filters=64, num_layers=4,
                       dim_reduction_type='avg_pooling', seed=0),
                config(experiment_name='exp_cnn_16_4_avg', num_epochs=10, num_filters=16, num_layers=4,
                       dim_reduction_type='avg_pooling', seed=0),
                ]

if not os.path.exists(experiment_config_target_json_dir):
    os.makedirs(experiment_config_target_json_dir)

def fill_template(script_text, config):

    for key, value in config.items():
        script_text = script_text.replace('${}$'.format(key), str(value))
    return script_text

def load_template(filepath):
    with open(filepath, mode='r') as filereader:
        template = filereader.read()

    return template

def write_text_to_file(text, filepath):
    with open(filepath, mode='w') as filewrite:
        filewrite.write(text)


for subdir, dir, files in os.walk(experiment_templates_json_dir):
    for template_file in files:
        filepath = os.path.join(subdir, template_file)
        for config in configs_list:
            loaded_template_file = load_template(filepath=filepath)
            config_dict = config._asdict()
            config_dict['experiment_name'] = "_".join([template_file.replace(".json", ""),
                                                       config.experiment_name])
            cluster_script_text = fill_template(script_text=loaded_template_file,
                                                config=config_dict)
            # name_customization = "_".join(str(item) for item in list(config._asdict().values()))
            cluster_script_name = '{}/{}_{}.json'.format(experiment_config_target_json_dir, template_file.replace(".json", ""),
                                                         config.experiment_name)
            cluster_script_name = os.path.abspath(cluster_script_name)
            write_text_to_file(cluster_script_text, filepath=cluster_script_name)
