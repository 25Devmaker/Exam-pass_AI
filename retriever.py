# retriever.py
# Job 1: Store chunks WITH metadata (semester, subject, unit, doc_type)
# Job 2: Retrieve chunks with optional metadata filtering
# This lets students filter by subject, semester, or doc type before searching

import chromadb
from embedder import embed_text, embed_chunks

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="exampass_syllabus",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks_with_metadata(embedded_chunks, metadata):
    # metadata = {semester, subject, unit, doc_type, source_file}
    # Every chunk from this PDF gets tagged with this metadata

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for chunk in embedded_chunks:
        # Unique ID includes file info so re-ingesting same file updates it
        chunk_id = (
            f"sem{metadata['semester']}"
            f"_{metadata['subject'].replace(' ', '_')}"
            f"_unit{metadata['unit']}"
            f"_{metadata['doc_type']}"
            f"_chunk{chunk['chunk_index']}"
            f"_page{chunk['page']}"
        )

        ids.append(chunk_id)
        embeddings.append(chunk["embedding"])
        documents.append(chunk["text"])

        # Store ALL metadata with each chunk
        metadatas.append({
            "page": chunk["page"],
            "semester": metadata["semester"],
            "subject": metadata["subject"],
            "unit": metadata["unit"] if metadata["unit"] else 0,
            "doc_type": metadata["doc_type"],
            "source_file": metadata["source_file"]
        })

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def retrieve(question, top_k=3, filters=None):
    # filters is optional dict to narrow search
    # Examples:
    #   filters={"semester": 3}
    #   filters={"subject": "Data Structures"}
    #   filters={"semester": 3, "doc_type": "lab_record"}
    #   filters={"subject": "DBMS", "unit": 2}

    question_vector = embed_text(question)

    # Build ChromaDB where clause from filters
    where = None
    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append({key: {"$eq": value}})

        # ChromaDB needs $and for multiple conditions
        if len(conditions) == 1:
            where = conditions[0]
        else:
            where = {"$and": conditions}

    # Query with or without filters
    query_params = {
        "query_embeddings": [question_vector],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }
    if where:
        query_params["where"] = where

    try:
        results = collection.query(**query_params)
    except Exception as e:
        # If filter returns no results, fall back to unfiltered
        print(f"⚠️  Filter returned no results, searching all documents...")
        query_params.pop("where", None)
        results = collection.query(**query_params)

    retrieved = []
    for i in range(len(results["documents"][0])):
        meta = results["metadatas"][0][i] or {}
        retrieved.append({
            "text": results["documents"][0][i],
            "page": meta.get("page", 1),
            "semester": meta.get("semester", ""),
            "subject": meta.get("subject", "Unknown"),
            "unit": meta.get("unit", ""),
            "doc_type": meta.get("doc_type", "Unknown"),
            "source_file": meta.get("source_file", "Unknown"),
            "similarity": 1 - results["distances"][0][i] if results["distances"] and results["distances"][0] else 0
        })

    return retrieved