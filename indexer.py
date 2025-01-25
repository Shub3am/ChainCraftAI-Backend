from langchain_community.document_loaders import PDFPlumberLoader
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from generateEmbedding import embeddings
from vectorDB import vectorStore
from vectorDB import persistClient
from langchain_ollama import OllamaLLM


def indexer():
        if (len(vectorStore.get()) ) :
              print("data already there, skipping")
              pass
        else: 
        
                loader = PDFPlumberLoader("./solidity.pdf")
                pages = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
                texts = text_splitter.split_documents(pages)
                vectorStore.from_documents(
                documents=texts,
            embedding=embeddings,
            collection_name="documentation",persist_directory="./chroma"     
        )


def getQuery(query):
            checks = vectorStore.similarity_search_with_score(query=query, k=4)
            joinPrompts = ""
            for i in checks:
                joinPrompts  = joinPrompts + i[0].page_content + '\n'
            return joinPrompts


def generateQuery(query, similarity_search):   
        LLM = OllamaLLM(model="qwen2.5-coder:7b")
        prompt = LLM.invoke("generate a dapp using solidity")
        print(prompt)
        
 

generateQuery("ge", "")
  