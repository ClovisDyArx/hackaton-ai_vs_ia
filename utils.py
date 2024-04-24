import os
import pandas as pd
import s3fs
import zipfile


def get_dataframe():
    # Create filesystem object
    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    # Télécharger les données dans le service
    PATH_IN = 'gvimont/diffusion/hackathon-minarm-2024/AIVSAI/HC3.zip'
    fs.download(PATH_IN, 'data/HC3.zip')
    with zipfile.ZipFile("data/HC3.zip", "r") as zip_file:
        zip_file.extractall("data/")

    # Concatenate subsets
    df = pd.DataFrame()
    for file in ['finance', 'open_qa', 'medicine', 'wiki_csai']:
        subset = pd.read_json("data/HC3/" + file + ".jsonl", lines=True)
        df = pd.concat([df, subset])

    df.reset_index(drop=True)
    return df


def get_new_dataframe():
    # Create filesystem object
    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    # Télécharger les données dans le service
    PATH_IN = "civel/diffusion/hackathon-minarm-2024/AIVSAI/hack_train.csv"
    fs.download(PATH_IN, "data/hack_train.csv")

    # Concatenate subsets
    df = pd.read_csv("data/hack_train.csv")
    return df
