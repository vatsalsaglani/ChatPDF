import os
import pinecone
from time import sleep

from config.config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV

from qa.completion import Completion
from qa.embedding_request import generate_embeddings


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


SYSTEM_PROMPT = "You are a helpful assistant. You have to use the provided extracted text chunks in triple backticks and answer the user query/question provided in single backticks. If the answer is not available in the extracted text you don't answer it."


class ChatPDF:
    def __init__(
        self, pinecone_api_key, pinecone_env, pinecone_index, pinecone_namespace
    ):
        self.complete = Completion(OPENAI_API_KEY)
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        self.namespace = pinecone_namespace
        self.index = pinecone.Index(pinecone_index)

    def __get_embedding__(self, question: str):
        embeddings = generate_embeddings([{"text": question, "src": "", "page_no": ""}])
        embedding = embeddings[0]
        embedding = embedding.get("embedding")
        return embedding

    def __search__(self, question: str):
        embedding = self.__get_embedding__(question)
        sim = self.index.query(
            embedding, top_k=10, include_metadata=True, namespace=self.namespace
        )
        texts = list(map(lambda s: s.get("metadata").get("text"), sim.get("matches")))
        return texts

    def __call__(self, message: str):
        search_results = self.__search__(message)

        message = f"""Extracted Text: ```{" ".join(search_results)}``` Question: `{message}`"""

        answer = ""
        for msg in self.complete(message, SYSTEM_PROMPT, "gpt-3.5-turbo-16k"):
            # print(msg)
            answer += msg
            clear_terminal()
            print(answer, end="", flush=True)
            sleep(0.1)


if __name__ == "__main__":
    cp = ChatPDF(PINECONE_API_KEY, PINECONE_ENV, "arxiv", "transformer-papers")
    while True:
        question = input("\nEnter your question: ")
        question = question.rstrip().lstrip()
        if question:
            cp(question)
        else:
            print("Please provide a question or query!")
            pass
