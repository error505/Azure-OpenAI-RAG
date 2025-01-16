import streamlit as st
from azure_ai_search import (
    create_index_if_not_exists,
    get_search_client,
    search_documents,
)
from open_ai_client import create_chatgpt_openai_client
from azure_open_ai_client import create_azure_openai_client
from document_processor import process_file, create_documents

# Create index if not already created
create_index_if_not_exists()
search_client = get_search_client()
# Give title to the page
st.title("OpenAI ChatGPT with File Upload and Azure AI Search")
# st.sidebar.title("OpenAI ChatGPT with File Upload and Azure AI Search")
# logo_url = "https://animatesvg.error505.com/logo.png"
# st.sidebar.image(logo_url, width=75)
# Sidebar for model selection
st.sidebar.title("ChatGPT Model Selection")
model_option = st.sidebar.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"])

# Sidebar for OpenAI API selection
api_option = st.sidebar.radio("Choose API", ["Azure OpenAI", "Native OpenAI"])


if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Create sidebar to adjust parameters
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1
)
max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=4096, value=256)
# File uploader functionality
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "md"])


if uploaded_file:
    # Process the file
    file_contents = process_file(uploaded_file)

    # Display file contents in sidebar
    st.sidebar.text_area("File Contents", value=file_contents, height=300)

    # Create documents for search indexing
    documents = create_documents(file_contents, uploaded_file)

    # Upload chunks to Azure AI Search
    search_client.upload_documents(documents=documents)

    st.sidebar.write("Uploaded chunks to Azure AI Search.")

    # Add the file content to the conversation for context
    st.session_state["messages"].append(
        {
            "role": "system",
            "content": "File content added to the conversation:" + file_contents,
        }
    )

# Update the interface with the previous messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create the chat interface
if prompt := st.chat_input("Enter your query"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Perform search in Azure AI Search index (RAG) if using Azure OpenAI
    if api_option == "Azure OpenAI":
        # Perform search and get results
        results = search_documents(prompt)  # Search the index for the query

        # Ensure the results contain both title and content for OpenAI to use
        title_line = ""
        for doc in results.split(
            "\n\n"
        ):  # Split results into individual document blocks
            # Here, you can process each document block to add title and content
            if "Title:" in doc and "Content:" in doc:
                title_line = doc.split("\n")[0]  # First line (Title)
        # Create the OpenAI client
        client = create_azure_openai_client()

        # Get response from the model with context from Azure AI Search
        response = client.chat.completions.create(
            model=model_option,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a helpful assistant which uses this context:\n{results} title:\n{title_line} "
                        "if any to answer the user question. If you have used the context for your answer please "
                        "add title of it as the reference in your answer."
                    ),
                },
                {"role": "user", "content": f"Context:\n{prompt}"},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Get the assistant's response
        assistant_reply = response.choices[0].message.content.strip()
    else:
        # If using native OpenAI, just generate a response based on user input
        client = create_chatgpt_openai_client()
        response = client.chat.completions.create(
            model=model_option,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        assistant_reply = response.choices[0].message.content.strip()

    # Display the assistant's reply
    st.session_state["messages"].append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
