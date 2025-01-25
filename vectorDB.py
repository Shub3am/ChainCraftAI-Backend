import chromadb
from langchain_chroma import Chroma
from generateEmbedding import embeddings

persistClient = chromadb.PersistentClient(path="./chroma")
persistClient.get_or_create_collection("documentation")

vectorStore = Chroma(client=persistClient,collection_name="documentation", embedding_function=embeddings, persist_directory="./chroma")
