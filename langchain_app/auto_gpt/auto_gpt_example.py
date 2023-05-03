"""This example shows how to use AutoGPT with a local model.
Unfortunately, it does NOT run as expected, the LLM gets lost,
so it's not really usable with current open models.

Tested on WizardLM 7b HF, 03.05.2023
- Paolo
"""

from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.experimental import AutoGPT

from langchain_app.models.text_generation_web_ui import build_text_generation_web_ui_client_llm

search = SerpAPIWrapper()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    WriteFileTool(),
    ReadFileTool(),
]



# Define your embedding model
embeddings_model = HuggingFaceInstructEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 768
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
llm = build_text_generation_web_ui_client_llm()

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=llm,
    memory=vectorstore.as_retriever()
)
# Set verbose to be true
agent.chain.verbose = True

agent.run(["write a weather report for SF today"])