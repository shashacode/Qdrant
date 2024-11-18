# Qdrant
This project was documented on my Medium page: https://medium.com/@floraoladipupo/optimizing-text-retrieval-with-multivector-search-and-payload-based-reranking-in-qdrant-a-case-ba970d365aad

The file titled Vectorss.py contains the code for the part of the article which talks about Creating a Qdrant collection, with appropriate payloads and showcasing different ways of payload filtering.
The TextEmbeddings.ipynb file contains the code for converting the Texts to Vectors using the SentenceTransformer library which was run on Google Colab GPU Instance
The text_retieval_task_dataset.csv is the csv file containing the texts to be converted to vectors which will be run on the Google Colab while the vectors.csv contains the output generated from the Google Colab. It contains the vectorized texts that will be used i the multi_search.py file.
The multi_search.py file contains the code for the part of the article talking about performing a multi-vector search that includes payload filtering. Also, rerank the final results using the payload


Overall the codes shows how to use Qdrant for Text retrieval utilizing Payload filtering, Vectors generation and multi vector search with reranking of payloads
