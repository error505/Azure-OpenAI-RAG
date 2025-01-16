from datetime import datetime
from docx import Document
import PyPDF2
from open_ai_client import create_chatgpt_openai_client
import numpy as np
from markitdown import MarkItDown

openai = create_chatgpt_openai_client()

md = MarkItDown()


# Function to get embedding from OpenAI for a given text chunk
def get_embedding(text: str):
    response = openai.embeddings.create(  # Correct method for embeddings
        model="text-embedding-ada-002",  # Embedding model to use
        input=text
    )
    # Correct way to access the embedding
    embedding = response.data[0].embedding  # Access data and embedding from the response
    return np.array(embedding)


def chunk_by_length(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def process_file(uploaded_file):
    file_contents = ""
    
    # Handle file based on type
    if uploaded_file.type == "text/plain":
        file_contents = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            file_contents += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        file_contents = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.type == "text/markdown":
        file_contents = md(uploaded_file.read().decode("utf-8"))
        
    return file_contents


def create_documents(file_contents, uploaded_file, chunk_size=1000):
    chunks = chunk_by_length(file_contents, chunk_size)
    return [
        {
            "id": f"chunk-{i}",
            "content": chunk,
            "file_name": uploaded_file.name,
            "file_path": uploaded_file.name,
            "file_type": uploaded_file.type,
            "file_size": len(file_contents),
            "file_created_at": datetime.now(),
            "file_updated_at": datetime.now(),
            "content_vector": get_embedding(chunk).tolist(),
        }
        for i, chunk in enumerate(chunks)
    ]
