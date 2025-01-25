from langchain_community.document_loaders import PDFPlumberLoader
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from generateEmbedding import embeddings
from vectorDB import vectorStore
from vectorDB import persistClient
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


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


def generateQuery(query,):   
        llm = OllamaLLM(model="tinyllama")
        LLM = OllamaLLM(model="qwen2.5-coder:3b")
        get_similarity_search_query = llm.invoke("Generate Queries for the documentation of Solidity for the project: " + query)
        RAG_data = getQuery(get_similarity_search_query)
        dapp_prompt_template = PromptTemplate.from_template("You have to build a complete dapp using solidity for the {topic} \n Here are the details from Solidity's Documentation: {docs} \n Seperate Each File in Markdown")
        promptGenerated = dapp_prompt_template.invoke({"topic": query, "docs": RAG_data})
        return promptGenerated
        
  