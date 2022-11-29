from google.cloud import storage

# import de diff settings pour les params

import random
import pickle
import json
import os


LOCAL_PATH=os.environ.get('LOCAL_PATH')
LOCAL_FILE_NAME=os.environ.get('LOCAL_FILENAME')

client = storage.Client()

# TODO : Local
def local_save(data, file_name=LOCAL_FILE_NAME):
        weights_folder_path = LOCAL_PATH
        if not os.path.exists(weights_folder_path):
            os.makedirs(weights_folder_path)

        file_name = os.path.join(weights_folder_path, file_name)
        with open(file_name, 'w') as f:
            f.write(data)

def local_read(file_name=LOCAL_FILE_NAME):
    weights_folder_path = LOCAL_PATH
    file_name = os.path.join(weights_folder_path, file_name)

    with open(file_name, 'r') as f:
        f.read()
        return f

# TODO : switch client / server done
def is_done() :
    with open(os.environ.get(LOCAL_FILE_NAME), 'r') as f:
        if 'client_done' or 'server_done' in f.read():
            return True
        return False


# TODO : Connect to the bucket
bucket = client.bucket(os.environ.get('BUCKET'))

# TODO : Save weights inside bucket
def bucket_save(bucket):
    pass

# TODO : Load weigths inside bucket
def load_weights():
    pass

# TODO : Load new weigths inside bucket
def load_new_weight():
    pass


if __name__ == '__main__':
     pass
