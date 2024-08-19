import os

import faiss
import numpy as np
from FlagEmbedding import BGEM3FlagModel

INDEX_FOLDER = 'index'

import logging

class VectorDatabase():
    def __init__(self, index_name='index', dimension=1024, threshold=0.2):
        self.dimension = dimension
        self.index_name = index_name
        self.embedding_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
        self.index_path = os.path.join(INDEX_FOLDER, f'{index_name}.index')
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:        
            self.index = faiss.IndexFlatL2(dimension)
        
        self.threshold = threshold
        
    def get_embedding(self, text):
        embedding = self.embedding_model.encode([text],
            batch_size=1,
            max_length=512,
        )['dense_vecs'].reshape(1, self.dimension).astype('float32')
        return embedding

    def check_threshold(self, embedding):
        distances, indices = self.index.search(embedding, 1)
        closest_distance = distances[0][0]
        logging.info(f"Closet distance: {closest_distance}")
        return closest_distance > self.threshold # True if the closest distance is greater than the threshold

    def add(self, embedding):
        self.index.add(embedding)
        faiss.write_index(self.index, self.index_path)