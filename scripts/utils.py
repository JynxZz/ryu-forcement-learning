import time

from google.cloud import storage
from stable_baselines3.common.logger import configure
from config import CFG
import numpy as np


def get_blob(name):
    client = storage.Client(CFG.project)
    bucket = client.bucket(CFG.bucket_path)
    blob = bucket.blob(f"{CFG.bucket_path}/{name}/")
    return blob


def get_timestamp(blob):
    blob.reload()
    return blob.time_created.timestamp()


def get_file_async(blob_path, file_path, timestamp):
    while True:
        time.sleep(CFG.wait_time)

        blob = get_blob(blob_path)
        try:
            blob_time = get_timestamp(blob)
        except:
            blob_time = 0

        if timestamp < blob_time:
            download(get_blob(blob_path), file_path)
            return


def download(blob, file):
    blob.download_to_filename(file)


def upload(blob, file):
    blob.upload_from_filename(file)


# Methode use by agent : buffer
def extract_buffer(buffer):
    # WARN Maybe we need to copy these arrays

    observation = buffer.observations
    action = buffer.actions
    reward = buffer.rewards
    episode_start = buffer.episode_starts
    value = buffer.values
    log_prob = buffer.log_probs

    return (
        observation,
        action,
        reward,
        episode_start,
        value,
        log_prob,
        buffer.returns,
        buffer.advantages,
    )


def concat_buffers(buffers):
    # Stack buffers
    assert len(buffers) > 2, "No buffer to add"
    n = len(buffers)
    init = buffers[0]

    a, b, c, d, e, f, g, h = init

    for j in range(n - 1):
        b = np.vstack([b, buffers[j + 1][1]])
        c = np.vstack([c, buffers[j + 1][2]])
        d = np.vstack([d, buffers[j + 1][3]])
        e = np.vstack([e, buffers[j + 1][4]])
        f = np.vstack([f, buffers[j + 1][5]])
        g = np.vstack([g, buffers[j + 1][6]])
        h = np.vstack([h, buffers[j + 1][7]])

        for key in init[0].keys():
            a[key] = np.vstack([a[key], buffers[j + 1][0][key]])

    return a, b, c, d, e, f, g, h


def load_buffer(data, buffer):
    (
        observations,
        actions,
        rewards,
        episode_starts,
        values,
        log_probs,
        returns,
        advantages,
    ) = data

    buffer.reset()
    buffer.buffer_size = CFG.buffer_size
    buffer.generator_ready = True

    buffer.observations = observations
    buffer.actions = actions
    buffer.rewards = rewards
    buffer.episode_starts = episode_starts
    buffer.values = values
    buffer.log_probs = log_probs
    buffer.returns = returns
    buffer.advantages = advantages
    buffer.pos = CFG.buffer_size
    buffer.full = True

    return buffer


if __name__ == "__main__":
    pass
