from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_app.models.vicuna_request_llm import VicunaLLM
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentType, initialize_agent

print("Creating embeddings...")
embeddings = SentenceTransformerEmbeddings()
with open("germany.txt") as f:
    book = f.read()


text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(book)
docsearch = Chroma.from_texts(
    texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]
)


print("Creating search tool...")
from pydantic import BaseModel, Field


class SearchInEmbeddings(BaseModel):
    query: str = Field()


def search(search_input: SearchInEmbeddings):
    docs = docsearch.similarity_search_with_score(search_input, k=1)
    return docs


tools = [
    Tool(
        name="Search",
        func=search,
        description="useful for when you need to answer questions about Germany",
    )
]

print("Initializing VicunaLLMClient")
memory = ConversationBufferMemory(memory_key="chat_history")
llm = VicunaLLM()
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, memory=memory
)

while True:
    query = input("Type your question: ")
    agent.run(input=query)
