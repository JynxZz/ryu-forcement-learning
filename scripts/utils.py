from google.cloud import storage
import pickle
import json
import os


BUCKET_PATH="../bucket-tmp"
FILE_NAME="unknow.pickle"


def save(file_name=FILE_NAME):
        weights_folder_path = BUCKET_PATH
        if not os.path.exists(weights_folder_path):
            os.makedirs(weights_folder_path)

        file_name = os.path.join(weights_folder_path, file_name)
        # torch.save(self.state_dict(), file_name)


# TODO : Connect to the bucket

# TODO : Load weigts inside bucket

# TODO : Connect to the VM

# TODO : Communication between VM & bucket


if __name__ == '__main__':
     pass
