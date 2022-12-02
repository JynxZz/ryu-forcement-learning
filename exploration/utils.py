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

def creation_date(path_to_file): # WIP -> Code ça putain : CHECK : ok
    try:
        timer = os.path.getmtime(path_to_file)
        return timer

    except OSError:
        return "Path '%s' does not exists or is inaccessible" %path_to_file
        # TODO : Save weights inside bucket : WIP -> good path ...
def bucket_save(project, bucket, agent, file_name):

    #client = storage.Client(project=os.environ.get('PROJECT'))
    client = storage.Client(project)

    #bucket = client.bucket(os.environ.get('BUCKET_TEST'))
    bucket = client.bucket(bucket)

    #blob = bucket.blob(f"{os.environ.get('STORAGE_LOCATION')}/{file}")
    blob = bucket.blob(f"{agent}/{agent+file_name}")

    # TODO utiliser blob.exists

    blob.upload_from_filename(file_name)

# TODO : Load weigths inside bucket : OK
def bucket_load(project, bucket, agent, file_name):

    #client = storage.Client(project=os.environ.get('PROJECT'))
    client = storage.Client(project)

    #bucket = client.bucket(os.environ.get('BUCKET_TEST'))
    bucket = client.bucket(bucket)

    #blob = bucket.blob(os.environ.get('STORAGE_LOCATION'))
    blob = bucket.blob(f"{agent}/{agent+file_name}")

    blob.download_to_filename(file_name)

    return blob



# TODO : method bucket general & timestamps
def old_interface_bucket(project, bucket, agent, file_name, timestamp, uploading=True):

    # TODO : Wrap inside method
    client = storage.Client(project)
    bucket = client.bucket(bucket)
    blob = bucket.blob(f"{agent}/{agent+file_name}")

    blob.reload()
    blob_timestamp = blob.time_created.timestamp()

    if uploading:
        blob.upload_from_filename(f'{agent+file_name}')
        print("Upload OK !")

    elif not uploading and blob_timestamp > timestamp :
        print("Switch OK")
        blob.download_to_filename(file_name)
        timestamp=blob_timestamp
        return timestamp
    else:
        pass

def switch(blob, timestamp):

    blob.reload()
    blob_timestamp = blob.time_created.timestamp()

    if blob_timestamp > timestamp:
        print("Switch OK")
        return True
    else:
        print("You Shall Not Pass")
        return False


def upload_download(blob, agent, file_name, uploading):

    if uploading:
        if file_name.endswith('.zip'):
            blob.upload_from_filename(file_name)
            print("Upload Server : OK !")
        else:
            blob.upload_from_filename(f'{agent+file_name}')
            print("Upload Client : OK !")

    elif not uploading:
        blob.download_to_filename(f'{agent+file_name}')
