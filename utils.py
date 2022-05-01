import requests
from tqdm.notebook import tqdm as tqdm
import os

def download_file(url, dest, override=False, chunksize=4096):
    if os.path.exists(dest) and not override:
        return
    with requests.get(url, stream=True) as r:
        try:
            file_size = int(r.headers["Content-Length"])
        except KeyError:
            file_size = 0
        chunks = file_size // chunksize

        with open(dest, "wb") as f, tqdm(
            total=file_size, unit="iB", unit_scale=True
        ) as t:
            for chunkdata in r.iter_content(chunksize):
                f.write(chunkdata)
                t.update(len(chunkdata))