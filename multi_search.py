import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
import pandas as pd
from io import StringIO
import csv

# Initialize Qdrant client
client = QdrantClient("localhost", port=6333)

# Load the data
file_path = r'c:\Users\ADMIN\Documents\Data_Science\vectors.csv'

# Open the CSV file and read its contents
with open(file_path, 'r') as file:
    content = file.read()

# Use StringIO to handle the CSV content as if it were a file
csv_data = StringIO(content)

# Create a CSV reader object to process the CSV data
reader = csv.DictReader(csv_data)

# Convert the CSV data to a list of dictionaries for easy processing
data = list(reader)

# Create a new collection
collection_name = "quotes"

# Check if collection exists and delete if it does
if client.get_collection(collection_name) is not None:
    client.delete_collection(collection_name)

# Create the collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
)

# Prepare points for insertion
points = []
search_requests = []
for item in data:
    vector = json.loads(item['vector'])
    points.append(
        models.PointStruct(
            id=int(item['id']),
            vector=vector,
            payload={
                "text": item['text'],
                "category": item['category'],
                "length": int(item['length']),
                "sentiment": item['sentiment']
            }
        )
    )
    search_requests.append(
        models.SearchRequest(
            vector=vector,
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(value='inspirational')
                    ),
                    models.FieldCondition(
                        key="sentiment",
                        match=models.MatchValue(value=item['sentiment'])
                    )
                ]
            ),
            with_payload=True,
            limit=2
        )
    )

# Insert points into the collection
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Created collection '{collection_name}' and inserted {len(points)} points.")

# Perform multi-vector search with payload filtering
search_result = client.search_batch(
    collection_name=collection_name,
    requests=search_requests
)

# Combine and deduplicate results
combined_results = {}
for batch in search_result:
    for hit in batch:
        if hit.id not in combined_results or hit.score > combined_results[hit.id].score:
            combined_results[hit.id] = hit

# Convert to list and sort by score
results = list(combined_results.values())
results.sort(key=lambda x: x.score, reverse=True)

# Rerank results using payload information
def rerank_score(hit):
    payload = hit.payload
    base_score = hit.score
    length_score = 1 - abs(payload['length'] - 45) / 45  # 45 is considered ideal length
    sentiment_score = 1 if payload['sentiment'] == 'positive' else 0.5

    final_score = base_score * (0.5 + length_score * 0.25 + sentiment_score * 0.25)

    return final_score

# Apply reranking
reranked_results = sorted(results, key=rerank_score, reverse=True)

# Print top 2 results after reranking
for i, hit in enumerate(reranked_results[:2], 1):
    print(f"{i}. ID: {hit.id}, Text: {hit.payload['text']}, "
          f"Original Score: {hit.score:.4f}, "
          f"Reranked Score: {rerank_score(hit):.4f}")
