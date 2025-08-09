import re
from typing import List

def split_text(text: str, chunk_size: int = 800, overlap: int = 200) -> List[str]:
    # Split by paragraphs, then further split if too long
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        while len(para) > chunk_size:
            chunks.append(para[:chunk_size])
            para = para[chunk_size - overlap:]
        if para:
            chunks.append(para)
    return chunks
