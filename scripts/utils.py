import time

import numpy as np
from google.cloud import storage
from google.cloud.storage import Blob
from stable_baselines3.common.buffers import RolloutBuffer

from config import CFG


def get_blob(name: str) -> Blob:
    client = storage.Client(CFG.project)
    bucket = client.bucket(CFG.bucket_path)
    if name == CFG.server_name:
        blob = bucket.blob(f"{CFG.weights_path}")
    else:
        blob = bucket.blob(f"{name}_obs.pickle")
        # blob = bucket.blob(f"{CFG.buffer_path}")
    return blob


def get_timestamp(blob: Blob) -> float:
    blob.reload()
    return blob.time_created.timestamp()


def get_file_async(name: str, file_path: str, timestamp: float) -> None:
    while True:
        time.sleep(CFG.wait_time)

        blob = get_blob(name)
        try:
            blob_time = get_timestamp(blob)
        except:
            blob_time = 0

        if timestamp < blob_time:
            download(get_blob(name), file_path)
            return


def download(blob: Blob, file: str) -> None:
    blob.download_to_filename(file)


def upload(blob: Blob, file: str) -> None:
    blob.upload_from_filename(file)


def extract_buffer(buffer: RolloutBuffer) -> tuple:

    return (
        buffer.observations,
        buffer.actions,
        buffer.rewards,
        buffer.episode_starts,
        buffer.values,
        buffer.log_probs,
        buffer.returns,
        buffer.advantages,
    )


def concat_buffers(buffers) -> tuple:
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


def load_buffer(data: tuple, buffer):
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