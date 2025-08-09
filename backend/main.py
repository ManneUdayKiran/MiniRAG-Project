
import requests
from bs4 import BeautifulSoup
from fastapi import Body

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List



from .file_utils import save_uploaded_files, clear_uploads_and_embeddings_if_empty
from .doc_parser import extract_text_from_file
from .text_splitter import split_text
from .embedding_store import embedding_store
from .llm_client import llm_client
from .kb_index import kb_index


app = FastAPI()

# Allow CORS for frontend
# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper to reload all tracked files/urls into embedding store
def reload_kb():
    embedding_store.clear()
    # Load files
    for fname in kb_index.get_files():
        fpath = os.path.join(os.path.dirname(__file__), "uploads", fname)
        if os.path.exists(fpath):
            with open(fpath, "rb") as f:
                class DummyUploadFile:
                    def __init__(self, file, filename):
                        self.file = file
                        self.filename = filename
                upload_file = DummyUploadFile(f, fname)
                text = extract_text_from_file(upload_file)
                chunks = split_text(text)
                embedding_store.add_texts(chunks)
    # Load URLs
    for url in kb_index.get_urls():
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            if len(text) > 20000:
                text = text[:20000]
            chunks = split_text(text)
            embedding_store.add_texts(chunks)
        except Exception:
            pass

# Endpoint to add content from a URL
@app.post("/add_url")
async def add_url(url: str = Body(..., embed=True)):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        if len(text) > 20000:
            text = text[:20000]
        chunks = split_text(text)
        kb_index.add_url(url)
        reload_kb()
        return {"status": "success", "chunks_added": len(chunks)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
    





@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    save_uploaded_files(files)
    for file in files:
        kb_index.add_file(file.filename)
    reload_kb()
    filenames = [file.filename for file in files]
    return {"filenames": filenames, "status": "processed"}


# New endpoint to delete a file and clear embeddings if no files remain
from fastapi import Query
import os


@app.delete("/delete_file")
async def delete_file(filename: str = Query(...)):
    file_path = os.path.join(os.path.dirname(__file__), "uploads", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    kb_index.remove_file(filename)
    reload_kb()
    return {"status": "deleted" if not os.path.exists(file_path) else "not found"}



@app.post("/ask")
async def ask_question(question: str = Form(...)):
    # Retrieve more context chunks
    contexts = embedding_store.search(question, top_k=8)
    # Deduplicate and filter empty chunks
    seen = set()
    unique_contexts = []
    for c in contexts:
        c_strip = c.strip()
        if c_strip and c_strip not in seen:
            unique_contexts.append(c_strip)
            seen.add(c_strip)
    context = "\n---\n".join(unique_contexts)
    # Call LLM via OpenRouter
    try:
        answer = llm_client.ask(question, context=context)
    except Exception as e:
        answer = f"[LLM ERROR] {str(e)}"
    return JSONResponse({
        "answer": answer,
        "context": context
    })

@app.get("/")
def root():
    return {"message": "Mini RAG FastAPI backend running."}
# List tracked files
@app.get("/list_files")
async def list_files():
    return {"files": kb_index.get_files()}

# List tracked URLs
@app.get("/list_urls")
async def list_urls():
    return {"urls": kb_index.get_urls()}

# Delete tracked URL
@app.delete("/delete_url")
async def delete_url(url: str = Body(..., embed=True)):
    kb_index.remove_url(url)
    reload_kb()
    return {"status": "deleted"}