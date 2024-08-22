
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np 

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dimension = 384  
index = faiss.IndexFlatL2(embedding_dimension)
transcriptions_dict = {}

def generate_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts] 
    return model.encode(texts).astype('float32')

def add_transcription_to_faiss(transcription, transcription_id):
    embeddings = generate_embeddings(transcription)
    if index.d != embeddings.shape[1]:
        raise ValueError(f"Index Dim ({index.d}) doesn't match with embeddings Dim({embeddings.shape[1]})")
    index.add(embeddings)  
    transcriptions_dict[transcription_id] = transcription
    print(f"Number of vectors in index: {index.ntotal}")    

def search_in_faiss(query_text):
    query_embedding = generate_embeddings([query_text])
    print(f"Query embedding shape: {query_embedding.shape}")  
    k = 3
    distances, indices = index.search(query_embedding, k) 
    print(f"Number of vectors in index: {index.ntotal}")
    if indices.ndim > 1:
        indices_flat = indices.flatten() 
    else:
        indices_flat = indices 

    results = []
    for idx in indices_flat:
        if idx >= 0:
            transcription_id = list(transcriptions_dict.keys())[idx]
            results.append(transcriptions_dict[transcription_id])
        else:
            results.append("Index not found")
    return results













