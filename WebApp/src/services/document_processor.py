from datetime import datetime
import streamlit as st
from src.services.open_ai_client import create_chatgpt_openai_client
import numpy as np
from markitdown import MarkItDown


# Initialize OpenAI and MarkItDown clients
openai = create_chatgpt_openai_client()
md = MarkItDown()


# Function to get embedding from OpenAI for a given text chunk
def get_embedding(text: str):
    response = openai.embeddings.create(  # Correct method for embeddings
        model="text-embedding-ada-002", input=text  # Embedding model to use
    )
    # Correct way to access the embedding
    embedding = response.data[
        0
    ].embedding  # Access data and embedding from the response
    return np.array(embedding)


# Function to chunk the text into smaller pieces
def chunk_by_length(text, chunk_size=500):

    # Ensure the text is a string and not empty
    if not isinstance(text, str) or not text.strip():
        raise ValueError("The text provided is either not a string or is empty.")

    clean_text = "".join(char if char.isprintable() else " " for char in text).strip()

    # Debugging the cleaned text length
    print(f"Cleaned text length: {len(clean_text)}")

    # Chunk the content into smaller parts
    chunks = [clean_text[i : i + 500] for i in range(0, len(clean_text), 500)]

    print(f"Number of chunks: {len(chunks)}")  # Debugging number of chunks

    return chunks


# Function to process file and extract text
def process_file(uploaded_file, type_of_file):
    file_contents = ""

    try:
        if type_of_file in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ]:
            # Read file as bytes and extract text using MarkItDown
            result = md.convert_stream(uploaded_file)
            file_contents = result.text_content  # Extract text using MarkItDown
            print("File contents:", file_contents)
        elif type_of_file in ["image/jpeg", "image/png"]:
            # For image files (JPEG, PNG), use OCR to extract text
            jp = MarkItDown(llm_client=openai, llm_model="gpt-4o")
            result = jp.convert_stream(uploaded_file)
            file_contents = result.text_content  # Use Tesseract OCR to extract text
        else:
            st.error(f"Unsupported file type: {type_of_file}")
            return None  # Handle unsupported file types

        if not file_contents:
            raise ValueError("No text content was extracted from the file.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None  # Ensure the function returns None if something goes wrong

    return file_contents  # Return the extracted text content


# Function to create documents from the extracted file content
def create_documents(file_contents, chunk_size=500, name=None, type_of_file=None):
    if not file_contents:
        st.error("No content available to create documents.")
        return []  # Return an empty list if no valid content is found

    # Chunk the content into smaller parts
    chunks = chunk_by_length(file_contents, chunk_size)

    if not chunks:
        st.error("No valid chunks created from the file content.")
        return []  # Return an empty list if no chunks were created

    return [
        {
            "id": f"chunk-{i}",
            "content": chunk,
            "file_name": name,
            "file_path": name,
            "file_type": type_of_file,
            "file_size": len(file_contents),
            "file_created_at": datetime.now(),
            "file_updated_at": datetime.now(),
            "content_vector": get_embedding(chunk).tolist(),
        }
        for i, chunk in enumerate(chunks)
    ]
