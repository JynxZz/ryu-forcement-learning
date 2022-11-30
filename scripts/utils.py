from google.cloud import storage

# import de diff settings pour les params

import random
import pickle
import json
import os


LOCAL_PATH=os.environ.get('LOCAL_PATH')
LOCAL_FILENAME=os.environ.get('LOCAL_FILENAME')


# TODO : Local
def local_save(data, file_name=LOCAL_FILENAME):
        weights_folder_path = LOCAL_PATH
        if not os.path.exists(weights_folder_path):
            os.makedirs(weights_folder_path)

        file_name = os.path.join(weights_folder_path, file_name)
        with open(file_name, 'w') as f:
            f.write(data)

def local_read(file_name=LOCAL_FILENAME):
    weights_folder_path = LOCAL_PATH
    file_name = os.path.join(weights_folder_path, file_name)

    with open(file_name, 'r') as f:
        f.readlines()

    return f

def creation_date(path_to_file):
    try:

        return os.path.getctime(path_to_file)
    except:

        pass


# TODO : switch client / server done
def is_done() :
    with open(os.environ.get(LOCAL_FILENAME), 'r') as f:
        if 'client_done' or 'server_done' in f.read():
            return True
        return False


# TODO : Connect to the bucket : OK

# TODO : Save weights inside bucket : OK
def bucket_save(file):

    client = storage.Client(project=os.environ.get('PROJECT'))
    bucket = client.bucket(os.environ.get('BUCKET_TEST'))
    blob = bucket.blob(f"{os.environ.get('STORAGE_LOCATION')}/{file}")

    blob.upload_from_filename(file)

# TODO : Load weigths inside bucket : OK
def load_weights(file):

    client = storage.Client()
    bucket = client.bucket(os.environ.get('BUCKET'))
    blob = bucket.blob(os.environ.get('STORAGE_LOCATION'))

    blob.download_to_filename(file)

    return blob

# TODO : Load new weigths inside bucket
def load_new_weight():
    pass


if __name__ == '__main__':
    #  local_save('coucou')
    print(creation_date("weights-agent-two.txt"))
