from google.cloud import storage

# import de diff settings pour les params

import random
import pickle
import json
import os


LOCAL_PATH=os.environ.get('LOCAL_PATH')
LOCAL_FILE_NAME=os.environ.get('LOCAL_FILENAME')

client = storage.Client()

# TODO : Local save
def local_save(file_name=LOCAL_FILE_NAME):
        weights_folder_path = LOCAL_PATH
        if not os.path.exists(weights_folder_path):
            os.makedirs(weights_folder_path)

        file_name = os.path.join(weights_folder_path, file_name)
        with open(file_name, 'w') as f:
            f.write(file_name)


# TODO : Connect to the bucket
bucket = client.bucket(os.environ.get('BUCKET'))

def is_done() :
    with open(os.environ.get(LOCAL_FILE_NAME)) as f:
        if 'blabla' in f.read():
            return True
        return False

# TODO : Save weights inside bucket
def bucket_save(bucket):
    pass

# TODO : Load weigths inside bucket
def load_weights():
    pass

# TODO : Load new weigths inside bucket
def load_new_weight():
    pass

# TODO : long & short train


if __name__ == '__main__':
     pass
