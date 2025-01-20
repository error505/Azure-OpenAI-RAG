import logging
from azure.cosmos import CosmosClient, exceptions
from src.utils.settings import AZURE_COSMOS_DB_CONNECTION_STRING, AZURE_COSMOS_DB_CONTAINER_NAME, AZURE_COSMOS_DB_DATABASE_NAME


connection_string = AZURE_COSMOS_DB_CONNECTION_STRING
client = CosmosClient.from_connection_string(connection_string)
database = client.get_database_client(AZURE_COSMOS_DB_DATABASE_NAME)
container_chats = database.get_container_client(AZURE_COSMOS_DB_CONTAINER_NAME)


def save_chat_to_cosmosdb(chat, user_id):
    """Save or update chat to Cosmos DB."""
    try:
        # Check if the chat already exists by user_id and chat_id
        existing_chat = container_chats.query_items(
            query=f"SELECT * FROM c WHERE c.user_id = '{user_id}' AND c.id = '{chat['id']}'",
            enable_cross_partition_query=True
        )

        # If chat already exists, upsert it with new messages
        if existing_chat:
            container_chats.upsert_item(chat)
            logging.info(f"Chat {chat['id']} updated in CosmosDB.")
        else:
            # If no existing chat, insert a new one
            container_chats.upsert_item(chat)
            logging.info(f"New chat {chat['id']} saved to CosmosDB.")

    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Error: Failed to save chat to Cosmos DB: {e}")


def get_chats():
    """
    Fetches all the chats.
    """
    query = "SELECT * FROM c"
    items = list(
        container_chats.query_items(
            query=query, enable_cross_partition_query=True
        )
    )

    # Fields to exclude
    exclude_fields = {"_rid", "_self", "_etag", "_attachments", "_ts"}

    filtered_items = [
        {key: value for key, value in item.items() if key not in exclude_fields}
        for item in items
    ]

    return filtered_items


# return items
def get_chat_by_id(chat_id, user_id):
    """
    Fetches a chat by its ID.
    """
    query = f"SELECT * FROM c WHERE c.id = '{chat_id}' and c.user_id = '{user_id}'" 
    items = list(
        container_chats.query_items(
            query=query, enable_cross_partition_query=True
        )
    )

    # Fields to exclude
    exclude_fields = {"_rid", "_self", "_etag", "_attachments", "_ts"}

    filtered_items = [
        {key: value for key, value in item.items() if key not in exclude_fields}
        for item in items
    ]

    return filtered_items[0] if filtered_items else None