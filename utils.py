import os
import pandas as pd
import s3fs
import zipfile
import glob

def get_dataframe(): 
    # Create filesystem object
    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    # Télécharger les données dans le service
    PATH_IN = 'gvimont/diffusion/hackathon-minarm-2024/AIVSAI/HC3.zip'
    fs.download(PATH_IN, 'data/HC3.zip')
    with zipfile.ZipFile("data/HC3.zip","r") as zip_file:
        zip_file.extractall("data/")

    #Concatenate subsets
    df = pd.DataFrame()
    for file in ['finance', 'open_qa', 'medicine', 'wiki_csai']:
        df = pd.concat([df, pd.read_json("data/HC3/" + file + ".jsonl", lines=True)])

    return df
