from qdrant_client import QdrantClient
from qdrant_client.http import models

# Initialize Qdrant client
client = QdrantClient("localhost", port=6333)

# Define the collection name
collection_name = "articles"

# Prepare the points with payloads
points = [
    models.PointStruct(
        id=1,
        vector=[0.1] * 384,
        payload={
            "title": "Introduction to Qdrant",
            "content": "Qdrant is a vector database management system...",
            "author": "John Doe",
            "date": "2023-07-01",
            "category": "Technology",
            "tags": ["database", "vector search", "Qdrant"],
            "views": 1000,
            "rating": 4.5
        }
    ),
    models.PointStruct(
        id=2,
        vector=[0.2] * 384,
        payload={
            "title": "Advanced Qdrant Techniques",
            "content": "This article covers advanced techniques in Qdrant...",
            "author": "Jane Smith",
            "date": "2023-07-15",
            "category": "Technology",
            "tags": ["Qdrant", "advanced", "optimization"],
            "views": 500,
            "rating": 4.8
        }
    ),
    models.PointStruct(
        id=3,
        vector=[0.3] * 384,
        payload={
            "title": "Vector Databases in Machine Learning",
            "content": "Vector databases play a crucial role in modern ML pipelines...",
            "author": "Alice Johnson",
            "date": "2023-08-01",
            "category": "Machine Learning",
            "tags": ["vector database", "machine learning", "AI"],
            "views": 750,
            "rating": 4.2
        }
    )
]

# Upsert the points into the collection
operation_info = client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Upsert operation completed. Status: {operation_info.status}")


# Exact Match Filtering

results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="Technology")
            )
        ]
    ),
    limit=10
)

# Range Filtering
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="views",
                range=models.Range(gte=500, lt=2000)
            )
        ]
    ),
    limit=10
)

# Multiple Condition Filtering
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
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
    limit=10
)

# Array Contains Filtering
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="tags",
                match=models.MatchAny(any=["Qdrant"])
            )
        ]
    ),
    limit=10
)

# Combining AND and OR Conditions
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        should=[
            models.FieldCondition(
                key="author",
                match=models.MatchValue(value="John Doe")
            ),
            models.FieldCondition(
                key="author",
                match=models.MatchValue(value="Jane Smith")
            )
        ],
        must=[
            models.FieldCondition(
                key="views",
                range=models.Range(gte=500)
            )
        ]
    ),
    limit=10
)

# Negative Filtering (NOT condition)
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        must_not=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="Sports")
            )
        ]
    ),
    limit=10
)

# Prefix Matching
results = client.search(
    collection_name="articles",
    query_vector=[0.1] * 384,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="title",
                match=models.MatchText(text="Intro")
            )
        ]
    ),
    limit=10
)