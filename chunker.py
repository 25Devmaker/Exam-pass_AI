# Job: Take the raw text from parser.py and split it into small overlapping chunks
# Why? Because we can't embed the entire PDF as one vector — we'd lose all detail
# Each chunk gets its own embedding and is stored separately in ChromaDB

def chunk_text(text, chunk_size=500, overlap=50):
    # chunk_size: how many words per chunk
    # overlap: how many words to repeat between chunks
    # Why overlap? So we don't cut a concept in half at a chunk boundary
    
    words=text.split()   # Step 1: Split the entire text into individual words
    chunks=[]   # Final list of chunks we'll return
    start=0    # Starting word index for current chunk

    while start<len(words):  
        end=start+chunk_size 
        chunk=" ".join(words[start:end])
        chunk=chunk.strip()

        if chunk:
            chunks.append({
                "text":chunk,
                "start_word":start,
                "end_word":end,
                "chunk_index":len(chunks)
            })
        start += chunk_size -overlap
    return chunks

def chunk_by_pages(parsed_result, chunk_size=500, overlap=50):
    all_chunks = []
    current_page = 1
    # parse_pdf returns a plain string; support both string and dict
    raw_text = parsed_result["text"] if isinstance(parsed_result, dict) else parsed_result
    pages = raw_text.split("--- Page")

    for page_block in pages:
        if not page_block.strip():
            continue
        lines= page_block.split("\n",1)

        try:
            page_num = int(lines[0].replace("---", "").strip())
            page_text = lines[1] if len(lines)>1 else""
        except:
            page_num=current_page
            page_text=page_block
        if not page_text.strip():
            current_page +=1
            continue

        page_chunks= chunk_text(page_text , chunk_size, overlap)

        for chunk in page_chunks:
            chunk["page"]=page_num
            all_chunks.append(chunk)

        current_page +=1
    return all_chunks
if __name__ == "__main__":
    from parser import parse_pdf

    result = parse_pdf("arrays.pdf")
    chunks= chunk_by_pages(result)

    print(f"total chunks created:{len(chunks)}")
    print(f"chunk 1 preview.")
    print(f"page:{chunks[0]['page']}")
    print(f"words:{chunks[0]['start_word']} -> {chunks[0]['end_word']}")
    print(f"text: {chunks[0]['text'][:200]}...")

    print(f"chunk-2 preview")
    print(f"page: {chunks[1]['page']}")
    print(f"text: {chunks[1]['text'][:200]}")

    print(f"\n overlap check")
    chunk1_words = chunks[0]['text'].split()[-10:]
    chunk2_words = chunks[1]['text'].split() [:10]
    print(f"end of chunk1 : {''.join(chunk1_words)}")
    print(f"start of chunk2 : {''.join(chunk2_words)}")

