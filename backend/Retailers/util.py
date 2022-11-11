import configparser
import os

def read_ini(file_path="Retailers/config.ini"):
    config = configparser.ConfigParser()
    config.read(file_path)    
    return config

def getUniqueItems(dicts, k:str = "itemName"):
    items = set()
    result = []
    for d in dicts:
        if not d[k] in items:
            items.add(d[k])
            result.append(d)
    return result
