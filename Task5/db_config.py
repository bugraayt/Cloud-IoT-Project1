# Task5/db_config.py  (corrected for serverless accounts)
from azure.cosmos import CosmosClient, PartitionKey
import os

# Edit these or, better, set them as environment variables
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://your-account.documents.azure.com:443/")
COSMOS_KEY = os.getenv("COSMOS_KEY", "your_primary_key_here")
DATABASE_NAME = os.getenv("DATABASE_NAME", "SmartHouseDB")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "Telemetry")

# Initialize client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Create DB if it doesn't exist
database = client.create_database_if_not_exists(id=DATABASE_NAME)

# Create container if it doesn't exist
# NOTE: Do NOT set offer_throughput on serverless accounts.
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/device_id")  # correct usage
)

print(f"Connected to Cosmos DB: {DATABASE_NAME}/{CONTAINER_NAME}")
