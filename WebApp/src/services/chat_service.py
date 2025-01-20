from src.services.azure_ai_search import search_documents
from src.services.open_ai_client import create_chatgpt_openai_client
from src.services.azure_open_ai_client import create_azure_openai_client
from src.services.azure_cosmos_db import save_chat_to_cosmosdb
import streamlit as st
from datetime import datetime, timezone
import uuid
from src.services.auth import check_authentication 
import tiktoken


def get_chat_response(prompt: str, api_option: str, model_option: str, temperature: float, max_tokens: int):
    if not check_authentication():
        raise Exception("User is not authenticated.")
    
    user_id = st.session_state.get("user_id", None)  # Get the user ID from the session state
    if not user_id:
        raise Exception("User ID not found, please authenticate again.")

    # If there is no chat_id in session state, create a new chat ID for this session
    if "chat_id" not in st.session_state:
        st.session_state["chat_id"] = str(uuid.uuid4())  # Generate unique chat ID for the session

    # Build the conversation history from the session state
    conversation_history = []
    if "current_chat" in st.session_state:
        conversation_history = st.session_state["current_chat"]
    else:
        st.session_state["current_chat"] = []

    # Append the new prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Call the respective function based on the API option
    if api_option == "Azure OpenAI":
        response, total_tokens, cost = _get_azure_openai_response(conversation_history, model_option, temperature, max_tokens)
    else:
        response, total_tokens, cost = _get_native_openai_response(conversation_history, model_option, temperature, max_tokens)

    # Append the response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})
    
    # Save updated conversation to session state
    st.session_state["current_chat"] = conversation_history

    # Prepare chat data for Cosmos DB
    chat_data = {
        "id": st.session_state["chat_id"],  # Use the existing chat ID
        "user_id": user_id,  # Save user ID
        "messages": conversation_history,
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Convert datetime to string
        "total_tokens": total_tokens,
        "cost": cost,
    }

    # Save chat to Cosmos DB (upsert to handle new and existing chats)
    save_chat_to_cosmosdb(chat_data, user_id)

    return response, total_tokens, cost


def _get_azure_openai_response(conversation_history, prompt: str, model: str, temperature: float, max_tokens: int):
    # Perform the document search to get relevant context from the documents
    results = search_documents(prompt)
    title_line = _extract_title_from_results(results)
    
    # Generate the prompt to send to the API
    system_content = (
        f"You are a helpful assistant which uses this context:\n{results} "
        f"title:\n{title_line} if any to answer the user question. If you "
        "have used the context for your answer please add the title of it as the reference in your answer."
    )
    
    # Append the user's prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Include the document context in the messages to send to the model
    messages = [{"role": "system", "content": system_content}] + conversation_history
    
    # Initialize OpenAI client and get the response
    client = create_azure_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract the output tokens from the response
    output_tokens = response.usage.total_tokens
    
    # Calculate total tokens
    total_tokens = sum(len(tiktoken.encoding_for_model(model).encode(msg['content'])) for msg in messages) + output_tokens
    cost = total_tokens * 0.002  # Example cost, adjust as needed

    return response.choices[0].message.content.strip(), total_tokens, cost


def _get_native_openai_response(conversation_history, model, temperature, max_tokens):
    client = create_chatgpt_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    # Extract the output tokens from the response
    output_tokens = response.usage.total_tokens

    # Calculate total tokens
    total_tokens = sum(len(tiktoken.encoding_for_model(model).encode(msg['content'])) for msg in conversation_history) + output_tokens
    cost = total_tokens * 0.002  # Example cost, assuming $0.002 per 1k tokens for Native OpenAI

    return response.choices[0].message.content.strip(), total_tokens, cost


def _extract_title_from_results(results: str) -> str:
    for doc in results.split("\n\n"):
        if "Title:" in doc and "Content:" in doc:
            return doc.split("\n")[0]
    return ""
