from distutils.log import error
import os
from typing import Callable,Union
import requests
import urllib.parse
PROJECT_ROOT = os.getcwd()
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# XOR function, P XOR R
def XOR(val1,val2) -> bool:
    return (val1 and not val2) or (val2 and not val1)
def error_handler(f: Callable) -> Union[Callable,bool]:
    def inner_function(args) -> None:
        try:
            return f(args)    
        except Exception as e:
            error(e)
            return False
    return inner_function
        
@error_handler
def download_data(url: str) -> bool:
    meta = os.path.join(DATA_DIR,'.datasets')
    data_file = urllib.parse.urlparse(url).path.split('/')[-1]
    file_path = os.path.join(DATA_DIR, data_file)
    if os.path.exists(meta):
        with open(meta, 'r') as fr:
            for line in fr:
                if line == data_file:
                    return True # if data_file found in metadata return True and exit(assume data is downloaded)
        # if entry not found in metadata file
        # attempt download
        res = requests.get(url)
        ## TODO: check Content-type if text
        with open(file_path, 'a') as fw:
            fw.write(res.text)
        return True
    else:
        print(f'Metadata file does not exist. Creating: {meta}')
        with open(meta, 'w') as fw:
            fw.write(data_file)
        # attempt download
        res = requests.get(url)
        ## TODO: check Content-type if text
        with open(file_path, 'a') as fw:
            fw.write(res.text)
        return True

