from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings 

embeddings = SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")

with open("germany.txt") as f:
    book = f.read()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(book)
docsearch = Chroma.from_texts(
    texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]
)

while True:
    query = input("Type your search: ")
    docs = docsearch.similarity_search_with_score(query, k=1)
    for doc in docs:
        print(doc)
