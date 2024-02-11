import os
import pandas as pd
import gzip
import json

DATAFOLDER = "hf_stack"
PARQUET_FILE = "hf_dataset.parquet"


def load_gzip_jsonl(file_path):
    data = []
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def create_hf_dataset():
    df = None
    for file in os.listdir(DATAFOLDER):
        data = load_gzip_jsonl(os.path.join(DATAFOLDER, file))
        if df is None:
            df = pd.DataFrame(data)
        else:
            df = pd.concat([df, pd.DataFrame(data)])

    # Save the dataset to a Parquet file
    df.to_parquet(PARQUET_FILE)


if __name__ == "__main__":
    create_hf_dataset()
