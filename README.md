# Mini RAG Project

A modern, full-stack Retrieval-Augmented Generation (RAG) app with a React  frontend and FastAPI backend. Upload documents (PDF, DOCX, image-based PDFs with OCR) or add web URLs, then ask questions and get answers strictly from your uploaded/added content.

## Features

- **Responsive UI**: Fully width on desktop, mobile-friendly, modern Ant Design components.
- **Hero Section**: Project title, description, and quick question input.
- **Modal Upload**: Add files or URLs via a modal dialog.
- **Knowledge Base**: Persistent list of uploaded files and URLs, with delete support.
- **Strict Context LLM**: Answers are generated only from your provided content.
- **Supported Formats**: PDF, DOCX, image-based PDFs (OCR), and web URLs.
- **Backend**: FastAPI, Sentence Transformers, FAISS, OpenRouter LLM, persistent JSON knowledge base.

## Getting Started

### Prerequisites

- Node.js (v18+ recommended)
- Python 3.9+

### Frontend Setup

```bash
cd MiniRAG-Project
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Optionally, set your OpenRouter API key in a .env file
uvicorn main:app --reload
```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

1. Open the app in your browser (default: http://localhost:5173).
2. Use the hero section to ask questions or click "Add File / URL" to upload documents or add web links.
3. Uploaded files and URLs are listed below, with options to delete.
4. Answers are generated strictly from your uploaded/added content.

## Project Structure

```
MiniRAG-Project/
├── backend/
│   ├── main.py
│   ├── kb_index.py
│   ├── doc_parser.py
│   ├── embedding_store.py
│   ├── llm_client.py
│   ├── kb_index.json
│   └── ...
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── components/
│   │   └── UploadModal.jsx
│   └── ...
└── ...
```

## Tech Stack

- **Frontend**: React, Vite, Ant Design, Axios
- **Backend**: FastAPI, Sentence Transformers, FAISS, PyPDF2, python-docx, pytesseract, pdf2image, BeautifulSoup, OpenRouter LLM

## License

MIT

---

_Built with ❤️ for rapid prototyping and learning._
