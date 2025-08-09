def clear_uploads_and_embeddings_if_empty(embedding_store):
    # If uploads directory is empty, clear embeddings
    if not os.listdir(UPLOAD_DIR):
        embedding_store.clear()
import os
from typing import List
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_files(files: List[UploadFile]):
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        file.file.seek(0)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        file.file.seek(0)  # Reset pointer so it can be read again for extraction
        saved_files.append(file_path)
    return saved_files
