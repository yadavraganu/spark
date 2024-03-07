from configparser import ConfigParser
import os

project_path = r"C:\Users\Anurag\Vs_Code_Projects\Spark"
config_path = os.path.join(project_path, 'config.ini')


def get_config(key, section='default'):
    cfg_par = ConfigParser()
    cfg_par.read(config_path)
    op = cfg_par[section][key]
    print(op)
    return op


if __name__ == "__main__":
    get_config('log_path')
