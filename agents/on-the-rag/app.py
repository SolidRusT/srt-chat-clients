import os
import gradio as gr
import chromadb
from mistralai import APIClient
from transformers import AutoTokenizer
import torch

# Mistral API
mistral_api_key = "jm1ghsXel9DRlX0mXAmyA0CQgyDkC2VB"
api_client = APIClient(api_key=mistral_api_key)

# ChromaDB
chroma_db = chromadb.Client()
collection = chromadb.Collection("documents")

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained("allenai/longformer-base-4096")

def encode_documents(documents):
    input_ids = tokenizer(documents, return_tensors="pt", truncation=True, padding=True).input_ids
    embeddings = api_client.embeddings(input_ids)
    return embeddings

def retrieve_documents(query, top_k=5):
    query_input_ids = tokenizer([query], return_tensors="pt", truncation=True, padding=True).input_ids
    query_embedding = api_client.embeddings(query_input_ids)

    results = collection.query(query_embedding, n_results=top_k)
    return [document for _, document in results]

def generate_response(query, documents):
    input_text = "\n".join([query] + documents)
    input_ids = tokenizer([input_text], return_tensors="pt", truncation=True, padding=True).input_ids
    outputs = api_client.generate(input_ids, max_length=100, num_return_sequences=1)
    return outputs[0]

def rag_app(query):
    documents = retrieve_documents(query)
    response = generate_response(query, documents)
    return response

def main():
    # Encode and add documents to the ChromaDB collection
    documents = [
        "Document 1 text...",
        "Document 2 text...",
        "Document 3 text..."
    ]
    embeddings = encode_documents(documents)
    collection.add(embeddings, documents)

    # Create Gradio interface
    gr.Interface(fn=rag_app, inputs="text", outputs="text", title="RAG App").launch()

if __name__ == "__main__":
    main()
