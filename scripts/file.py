from google.cloud.storage import Blob, Client

import pickle
import time
import pathlib


class File:
    PROJECT = "nice-psyche-370808"
    BUCKET = "chun-li"

    def __init__(self, path: str) -> None:
        self.path = path
        self.blob = self._set_blob()
        # TODO Maybe get the blob timestamp here.
        self.time = time.time()

    def _set_blob(self) -> Blob:
        client = Client(self.PROJECT)
        bucket = client.bucket(self.BUCKET)
        return bucket.blob(self.path)

    def _refresh(self) -> None:
        self.blob.reload()

    def exists(self) -> bool:
        return self.blob.exists()

    def get_timestamp(self) -> float:
        self._refresh()
        return self.blob.time_created.timestamp()

    def get_update(self) -> None:
        while True:
            time.sleep(1)
            blob_time = 0
            if self.exists():
                blob_time = self.get_timestamp()
            if self.time < blob_time:
                self.time = blob_time
                return

    def upload(self) -> None:
        self.blob.upload_from_filename(self.path)

    def download(self) -> None:
        self.blob.download_to_filename(self.path)

    def to_pickle(self, data) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(data, f)

    def from_pickle(self):
        with open(self.path, "rb") as file:
            return pickle.load(file)
