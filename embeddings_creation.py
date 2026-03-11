import requests
import json
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

#Creating a function to embedd the chunks

def create_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list
    })

    embedding=r.json()['embeddings']
    return embedding

#Reading the json file
jsons=os.listdir("new_jsons")

my_dicts=[]

chunk_id=0 # For giving sequence number to chunks
for json_file in jsons:
    with open(f"new_jsons/{json_file}") as f:
        content=json.load(f)
        print(f"Creating_Embeddings for {json_file}")

#Calling the embedding func and giving the text and chunks
        embeddings=create_embedding([c['text'] for c in content['chunks']])

#Iterating the chunk and using enumerate function to give the index
        for i,chunk in enumerate(content['chunks']):
            chunk['chunk_id']=chunk_id
            chunk['embedding']=embeddings[i]
            chunk_id+=1
            my_dicts.append(chunk)

#Converting the embedded chunks into dataframe and saving it as joblib file for later use in process_incoming.py
df=pd.DataFrame.from_records(my_dicts)
joblib.dump(df,'new_embeddings.joblib')
