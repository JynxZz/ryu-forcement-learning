from google.cloud import storage
from stable_baselines3.common.logger import configure
from scripts.config import CFG
import numpy as np


# TODO : Wrap 3 method
def get_blob_client():

    client = storage.Client(CFG.project)
    bucket = client.bucket(CFG.bucket_path)
    blob = bucket.blob(CFG.client_path)
    return blob


def get_blob_server():

    client = storage.Client(CFG.project)
    bucket = client.bucket(CFG.bucket_path)
    blob = bucket.blob(CFG.server_path)
    return blob


def get_timestamp(blob):
    blob.reload()
    return blob.time_created.timestamp()


def download(blob, file):
    blob.download_to_filename(file)


def upload(blob, file):
    blob.upload_from_filename(file)


# Methode use by agent : buffer
def extract_buffer(client_agent):

    # WARN Maybe we need to copy these arrays

    # Extracting buffer
    buffer = client_agent.rollout_buffer
    observation = buffer.observations
    action = buffer.actions
    reward = buffer.rewards
    episode_start = buffer.episode_starts
    value = buffer.values
    log_prob = buffer.log_probs

    to_buffer = (
        observation,
        action,
        reward,
        episode_start,
        value,
        log_prob,
        buffer.returns,
        buffer.advantages,
    )

    return to_buffer


def concat_buffer(buffers):
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

    return (a, b, c, d, e, f, g, h)


def load_buffer(imported_obs, server_agent):

    (
        observations,
        actions,
        rewards,
        episode_starts,
        values,
        log_probs,
        returns,
        advantages,
    ) = imported_obs

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

    buffer.pos = len(imported_obs[5])

    buffer.full = True

    return server_agent.rollout_buffer


if __name__ == "__main__":

    pass
