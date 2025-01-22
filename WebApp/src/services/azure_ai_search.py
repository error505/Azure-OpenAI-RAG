from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from src.utils.settings import AZURE_AI_SEARCH_ENDPOINT, AZURE_AI_SEARCH_API_KEY, AZURE_AI_SEARCH_INDEX_NAME
from azure.search.documents.indexes.models import (
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchAlgorithmKind,
    HnswParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearchProfile,
    VectorSearchAlgorithmMetric,
)
from src.services.document_processor import get_embedding
from src.services.document_processor import process_file, create_documents


# Azure Search setup
search_endpoint = AZURE_AI_SEARCH_ENDPOINT
search_api_key = AZURE_AI_SEARCH_API_KEY
index_name = AZURE_AI_SEARCH_INDEX_NAME

# Create a SearchIndexClient to manage indexes
index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_api_key))


# Check if the index exists, create it if not
def create_index_if_not_exists():
    try:
        # Try to fetch the index to see if it exists
        index_client.get_index(index_name)
    except Exception:
        # If the index doesn't exist, create it
        print("Index not found. Creating new index...")
        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="defaultHnsw",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(
                        metric=VectorSearchAlgorithmMetric.COSINE,  # Use cosine similarity
                        m=4,  # Number of connections in the graph
                        ef_construction=400,  # Efficiency parameter during the index construction
                        ef_search=500  # Efficiency parameter during search
                    ),
                )
            ],
            profiles=[
                VectorSearchProfile(name="HnswVectorSearchProfile", algorithm_configuration_name="defaultHnsw"),
            ],
        )
        content_vector_field = SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  # A collection of floats for the vector
            searchable=True,  # We want to make it searchable based on vector similarity
            hidden=False,  # Visible for search purposes
            vector_search_dimensions=1536,  # Length of the embedding vector (e.g., 1536 for OpenAI embeddings)
            vector_search_profile_name="HnswVectorSearchProfile",  # The vector search profile
        )
        index = SearchIndex(
            name=index_name,
            fields=[
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SimpleField(name="file_name", type=SearchFieldDataType.String),
                SimpleField(name="file_path", type=SearchFieldDataType.String),
                SimpleField(name="file_type", type=SearchFieldDataType.String),
                SimpleField(name="file_size", type=SearchFieldDataType.Int64),
                SimpleField(name="file_created_at", type=SearchFieldDataType.DateTimeOffset),
                SimpleField(name="file_updated_at", type=SearchFieldDataType.DateTimeOffset),
                SearchableField(name="content", type=SearchFieldDataType.String),
                content_vector_field
            ],
            vector_search=vector_search
        )
        index_client.create_or_update_index(index)
        print("Index created.")


# Create index if not already created
create_index_if_not_exists()


def get_search_client():
    # Create the SearchClient for document operations
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_api_key)
    )
    return search_client


def search_documents(query):
    # Perform a search in the index
    search_client = get_search_client()

    # Generate the query vector from the input text using your embedding model
    query_vector = get_embedding(query).tolist()  # Get the embedding for the query

    # Debugging: Print the query vector to ensure it’s being generated correctly
    print(f"Query vector: {query_vector}")

    # Construct the vector query with the 'kind' parameter set to "vector"
    vector_query = {
        "vector": query_vector,  # The query vector (embedding)
        "field_name": "content_vector",  # The field to search (the one containing the embeddings)
        "k_nearest_neighbors": 10,  # Number of nearest neighbors to return
        "kind": "vector",  # Specify the search type, such as nearest neighbor search
        "fields": "content_vector",  # Explicitly set the vector field to be searched
        "weight": 1.0,  # Optional: Set the weight for the query (default is 1.0)
    }

    # Execute the search query with vector query, scoring profile, filters, etc.
    try:
        results = search_client.search(
            search_text="",  # Leave empty for pure vector search
            vector_queries=[vector_query],  # Pass the vector query to the search
            top=10  # Limit to top 10 results
        )
    except Exception as e:
        print(f"Error during search: {e}")
        return "Error occurred during the search."

    # Convert the results from the iterator to a list (if needed)
    results_list = list(results)

    # Create a context with title and content for OpenAI
    context = ""
    for doc in results_list:
        title = doc.get("file_name", "Unknown Title")  # Get the title (PDF file name)
        content = doc.get("content", "No content found")  # Get the content of the document
        context += f"Title: {title}\nContent: {content}\n\n"

    # Debugging: Print the context to check its format
    print("Context for OpenAI:")
    print(context)

    # Display high-scoring results (for debugging)
    for result in results_list:
        print(f"Document ID: {result['id']}, Title: {result['file_name']}, Score: {result['@search.score']}, Content: {result.get('content', 'No content found')}")

    return context


def handle_upload_documents(documents, type_of_file, name):
    create_index_if_not_exists()
    # Upload documents to Azure AI Search
    file_contents = process_file(documents, type_of_file)

    # Create documents for search indexing
    documents = create_documents(file_contents, name, type_of_file)

    # Upload chunks to Azure AI Search
    search_client = get_search_client()
    search_client.upload_documents(documents=documents)
    print("Documents uploaded to Azure AI Search.")
