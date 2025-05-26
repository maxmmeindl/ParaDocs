# query.py
import os
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# If you updated ingest.py to langchain_community, do the same here:
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

embeddings   = OpenAIEmbeddings()
vector_store = FAISS.load_local("paradocs_faiss", embeddings)

chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
)

question = input("🔍 Question: ")
print("\n📝 Answer:\n", chain.run(question))
