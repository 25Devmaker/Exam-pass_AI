# embedder.py
# Job: Convert chunks into vectors using a local model
# sentence-transformers runs 100% on your machine — no API key, no credits, free forever
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["HUGGINGFACE_HUB_TOKEN"] = os.getenv("HF_TOKEN")
from sentence_transformers import SentenceTransformer

# Load the model — downloads once (~90MB), cached locally after that
# all-MiniLM-L6-v2 is fast, lightweight, and great for educational content
model = SentenceTransformer("microsoft/codebert-base")

# Note: this model produces 384 dimensions vs OpenAI's 1536
# Smaller but plenty powerful for our use case


def embed_text(text):
    # Takes a single string, returns a vector
    embedding = model.encode(text)
    return embedding.tolist()  # Convert numpy array to plain list


def embed_chunks(chunks):
    print(f"Embedding {len(chunks)} chunks locally...")

    # Extract just the text from each chunk for batch embedding
    # Batch embedding is faster than one by one
    texts = [chunk["text"] for chunk in chunks]

    # Embed all at once — sentence-transformers handles batching internally
    vectors = model.encode(texts, show_progress_bar=True)

    embedded_chunks = []
    for i, chunk in enumerate(chunks):
        embedded_chunks.append({
            "text": chunk["text"],
            "page": chunk["page"],
            "chunk_index": chunk["chunk_index"],
            "embedding": vectors[i].tolist()
        })

    print(f"✅ All {len(chunks)} chunks embedded successfully")
    return embedded_chunks


if __name__ == "__main__":
    from parser import parse_pdf
    from chunker import chunk_by_pages

    result = parse_pdf("arrays.pdf")
    chunks = chunk_by_pages(result)

    embedded = embed_chunks(chunks)

    print(f"\n--- VECTOR PREVIEW ---")
    print(f"Chunk 1 text: {embedded[0]['text'][:100]}...")
    print(f"Chunk 1 page: {embedded[0]['page']}")
    print(f"Vector length: {len(embedded[0]['embedding'])} dimensions")
    print(f"First 5 values: {embedded[0]['embedding'][:5]}")