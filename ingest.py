import os, requests, re
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import mammoth
from langchain.schema import Document

load_dotenv()
# (ensure OPENAI_API_KEY is in .env)

OWNER = "maxmmeindl"
REPO  = "ParaDocs"
BRANCH= "main"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/docs?ref={BRANCH}"

# 1) list all files in /docs
resp = requests.get(API_URL)
resp.raise_for_status()
items = resp.json()

# 2) filter for our extensions
exts = {".pdf", ".docx", ".xlsx", ".md"}
links = [
    item["name"]
    for item in items
    if os.path.splitext(item["name"].lower())[1] in exts
]

os.makedirs("downloaded", exist_ok=True)
docs = []

for name in links:
    # raw URL for each
    raw = (
      f"https://raw.githubusercontent.com/"
      f"{OWNER}/{REPO}/{BRANCH}/docs/{name}"
    )
    r = requests.get(raw)
    r.raise_for_status()

    local = os.path.join("downloaded", name)
    with open(local, "wb") as f:
        f.write(r.content)
    print("Downloaded", name)

    # extract text
    lower = name.lower()
    if lower.endswith(".pdf"):
        reader = PdfReader(local)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    elif lower.endswith(".docx"):
        text = mammoth.extract_raw_text(open(local, "rb")).value
    elif lower.endswith(".xlsx"):
        # Skip Excel files for now as they require special handling
        print(f"Skipping Excel file: {name}")
        continue
    else:
        text = open(local, encoding="utf8").read()

    docs.append(Document(page_content=text, metadata={"source": name}))

# 3) split & embed
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
store  = FAISS.from_documents(chunks, OpenAIEmbeddings())
store.save_local("paradocs_faiss")

print("Done - Vector store saved in 'paradocs_faiss/'")
