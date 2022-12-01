from google.cloud import storage
from stable_baselines3.common.logger import configure


# import de diff settings pour les params

import numpy as np
import pickle
import random
import os
import datetime, time


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


# TODO : switch client / server done

now = time.time()
init_timestamp = time.time() # WIP -> find the good type timestamp : CHECK : ok

def switch(old_timestamp):

    timestamp = creation_date()

    if old_timestamp < timestamp:
        old_timestamp = timestamp
        return old_timestamp, True

    return old_timestamp, False

def creation_date(path_to_file): # WIP -> Code ça putain : CHECK : ok
    try:
        timer = os.path.getmtime(path_to_file)
        return timer

    except OSError:
        return "Path '%s' does not exists or is inaccessible" %path_to_file



# TODO : Connect to the bucket : OK



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

# TODO : Wrap 3 method
def interface_bucket(project, bucket, agent, file_name):
    try:
        client = storage.Client(project)
        bucket = client.bucket(bucket)
        blob = bucket.blob(f"{agent}/{agent+file_name}")
        return blob
    except:
        return "Path '%s' does not exists or is inaccessible" %blob


def get_timestamp(blob) -> float:
    blob.reload()
    return blob.time_created.timestamp()

def switch(blob, timestamp):

    blob.reload()
    blob_timestamp = blob.time_created.timestamp()

    if blob_timestamp > timestamp:
        print("Switch OK")
        return True
    else:
        print("You Shall Not Pass")
        return False

def max_download(blob, file):
    blob.download_to_filename(file)

def jynxzz_upload(blob, file):
    blob.upload_from_filename(file)

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

# Methode use by the Server & Client
def extract_buffer(client_agent):

    # WARN Maybe we need to copy these arrays

    #Extracting buffer
    buffer = client_agent.rollout_buffer
    observation = buffer.observations
    action = buffer.actions
    reward = buffer.rewards
    episode_start = buffer.episode_starts
    value = buffer.values
    log_prob = buffer.log_probs

    to_buffer = (observation, action,
                 reward, episode_start,
                 value, log_prob,
                 buffer.returns, buffer.advantages)

    for item in to_buffer:
        print(type(item))

    return to_buffer


def concat_buffer(buffers):
    #Stack buffers
    assert len(buffers)>2, "No buffer to add"
    n=len(buffers)
    init = buffers[0]

    a, b, c, d, e, f, g, h = init
    # a = init[0]
    # b = init[1]
    # c = init[2]
    # d = init[3]
    # e = init[4]
    # f = init[5]
    # g = init[6]
    # h = init[7]
    #print(np.vstack([b,buffers[1][1]]))
    for j in range(n-1):
        b = np.vstack([b,buffers[j+1][1]])
        c = np.vstack([c,buffers[j+1][2]])
        d = np.vstack([d,buffers[j+1][3]])
        e = np.vstack([e,buffers[j+1][4]])
        f = np.vstack([f,buffers[j+1][5]])
        g = np.vstack([g,buffers[j+1][6]])
        h = np.vstack([h,buffers[j+1][7]])

        for key in init[0].keys():
            a[key]=np.vstack([a[key],buffers[j+1][0][key]])

    return (a,b,c,d,e,f,g,h)

# TODO Pass buffer, not full agent
def load_buffer(imported_obs, server_agent):

    observations, actions, rewards, episode_starts, values, log_probs, returns, advantages = imported_obs

    buffer = server_agent.rollout_buffer

    buffer.reset()
    buffer.buffer_size = server_agent.n_steps
    buffer.generator_ready = True

    buffer.observations = observations
    buffer.actions = actions
    buffer.rewards = rewards
    buffer.episode_starts = episode_starts
    buffer.values = values
    buffer.log_probs = log_probs
    buffer.returns = returns
    buffer.advantages = advantages

    buffer.pos=len(imported_obs[5])

    buffer.full=True

    return server_agent.rollout_buffer

def evaluate(model):
    env_settings['continue_game']=0
    env,_ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)
    obs = env.reset()
    rew = []
    for i in range(5):

        tot =0
        while True:

            action, _ = model.agent.predict(obs, deterministic=True)

            obs, reward, done, info = env.step(action)
            tot+=reward[0]
            if done:
                obs = env.reset()
                if info[0]["game_done"]:
                    print(tot)
                    rew.append(tot)
                    break
    env.close()
    env_settings['continue_game']=1
    return np.array(rew).mean()

if __name__ == '__main__':


    print(init_timestamp)
    print(creation_date("readme.md"))
    print(now)

    project = os.environ['PROJECT']
    bucket = os.environ['BUCKET_TEST']
    agent = os.environ['AGENT_NAME']
    server = os.environ['SERVER_NAME']
    file_name = os.environ['OBS']




    bucket_save(project, bucket, agent, file_name)
    bucket_load(project, bucket, agent, file_name)
