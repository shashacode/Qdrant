from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np

# Initialize Qdrant client
client = QdrantClient("localhost", port=6333)

# Define the collection name
collection_name = "articles"

# Define multiple query vectors (simulating different aspects of the search)
query_vector1 = np.random.rand(384).tolist()  # Main content vector
query_vector2 = np.random.rand(384).tolist()  # Title vector

# Perform multi-vector search with payload filtering
search_result = client.search_batch(
    collection_name=collection_name,
    requests=[
        models.SearchRequest(
            vector=query_vector1,
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(value="Technology")
                    ),
                    models.FieldCondition(
                        key="rating",
                        range=models.Range(gte=4.0)
                    )
                ]
            ),
            with_payload=True,
            limit=20
        ),
        models.SearchRequest(
            vector=query_vector2,
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(value="Technology")
                    ),
                    models.FieldCondition(
                        key="rating",
                        range=models.Range(gte=4.0)
                    )
                ]
            ),
            with_payload=True,
            limit=20
        )
    ]
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
    
    # Adjust score based on views (assuming more views is better)
    view_boost = min(payload['views'] / 1000, 1)  # Cap at 1
    
    # Adjust score based on recency of the article
    from datetime import datetime
    date = datetime.strptime(payload['date'], "%Y-%m-%d")
    days_old = (datetime.now() - date).days
    recency_boost = max(1 - (days_old / 365), 0)  # Newer articles get higher boost
    
    # Adjust score based on rating
    rating_boost = payload['rating'] / 5  # Assuming rating is out of 5
    
    # Combine all factors
    final_score = base_score * (1 + view_boost + recency_boost + rating_boost) / 4
    
    return final_score

# Apply reranking
reranked_results = sorted(results, key=rerank_score, reverse=True)

# Print top 2 results after reranking
for i, hit in enumerate(reranked_results[:5], 1):
    print(f"{i}. ID: {hit.id}, Title: {hit.payload['title']}, "
          f"Original Score: {hit.score:.4f}, "
          f"Reranked Score: {rerank_score(hit):.4f}")
    
