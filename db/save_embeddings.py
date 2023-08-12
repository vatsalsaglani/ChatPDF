import pinecone
from typing import List, Dict, Union
from tqdm.auto import tqdm, trange


class PineconeDB:
    def __init__(
        self,
        api_key: str,
        environment: str,
        index_name: str,
        namespace: Union[str, None] = None,
        batch_size: int = 50,
    ):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
        self.batch_size = batch_size
        self.namespace = namespace

    def __store__(self, embeddings: List[Dict]):
        for ix in trange(0, len(embeddings), self.batch_size, desc="Storing Vectors"):
            pvs = []
            for ixe, embs in enumerate(embeddings[ix : ix + self.batch_size]):
                if len(embs.get("embedding")) > 0:
                    e = embs.get("embedding")
                    del embs["embedding"]
                    pvs.append((str(ix + ixe), e, {**embs}))
            if self.namespace:
                self.index.upsert(vectors=pvs, namespace=self.namespace)
            else:
                self.index.upsert(vectors=pvs)

    def __call__(self, embeddings: List[Dict]):
        self.__store__(embeddings)
