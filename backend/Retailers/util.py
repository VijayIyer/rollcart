import configparser
import os

def read_ini(file_path="Retailers/config.ini"):
    config = configparser.ConfigParser()
    config.read(file_path)    
    return config
