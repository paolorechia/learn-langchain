from langchain_app.models.vicuna_embeddings import VicunaEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

with open("plato_laws.txt") as f:
    plato = f.read()

text_splitter = CharacterTextSplitter(chunk_size=128, chunk_overlap=0)
texts = text_splitter.split_text(plato)
embeddings = VicunaEmbeddings()
docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])

while True:
    query = input("Type your search: ")
    docs = docsearch.similarity_search_with_score(query)
    for doc in docs:
        print(doc)
