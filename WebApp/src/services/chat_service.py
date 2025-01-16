from src.services.azure_ai_search import search_documents
from src.services.open_ai_client import create_chatgpt_openai_client
from src.services.azure_open_ai_client import create_azure_openai_client


def get_chat_response(prompt: str, api_option: str, model_option: str, temperature: float, max_tokens: int) -> str:
    if api_option == "Azure OpenAI":
        return _get_azure_openai_response(prompt, model_option, temperature, max_tokens)
    return _get_native_openai_response(prompt, model_option, temperature, max_tokens)


def _get_azure_openai_response(prompt: str, model: str, temperature: float, max_tokens: int) -> str:
    results = search_documents(prompt)
    title_line = _extract_title_from_results(results)
    
    client = create_azure_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a helpful assistant which uses this context:\n{results} "
                    f"title:\n{title_line} if any to answer the user question. If you "
                    "have used the context for your answer please add title of it as "
                    "the reference in your answer."
                ),
            },
            {"role": "user", "content": f"Context:\n{prompt}"},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def _get_native_openai_response(prompt: str, model: str, temperature: float, max_tokens: int) -> str:
    client = create_chatgpt_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def _extract_title_from_results(results: str) -> str:
    for doc in results.split("\n\n"):
        if "Title:" in doc and "Content:" in doc:
            return doc.split("\n")[0]
    return ""
