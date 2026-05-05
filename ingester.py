import os
from parser import parse_pdf
from retriever import store_chunks_with_metadata
from chunker import chunk_by_pages
from embedder import embed_chunks 

PDF_ROOT = "PDF data"

VALID_TYPES=["notes", "ppt", "lab_record", "imp_questions"]

def parse_filename(filename, semester):
    name= filename.replace(".pdf", "").lower()
    parts = name.split("_")

    doc_type= "notes"
    for valid in VALID_TYPES:
        if name.endswith(valid.replace("_","")):
            doc_type = valid
            break
        if "lab_record" in name or "labrecord" in name:
            doc_type = "lab_record"
            break
        if "ppt" in name:
            doc_type = "ppt"
            break 
        if "imp_questions" in name:
            doc_type = "imp_questions"
            break 
    unit = None
    for part in parts:
        if part.startswith("unit") and len(part)>4:
            try:
                unit= int(part.replace("unit", ""))
            except:
                pass

    if parts[0].startwith("sem"):
        parts = parts[:1]
    subject_parts=[]
    for part in parts:
        if part.startswith("unit") or part in ["notes", "ppt", "lab_record", "imp_questions"]:
            break
        subject_parts.append(part)
    subject = " ".join(subject_parts).title()
    if not subject:
        subject = filename.replace(".pdf", "")
    return{
        "semester":semester,
        "subject":subject,
        "unit":unit,
        "doc_type":doc_type,
        "source_file":filename
    }        

def ingest_all():
    if not os.path.exists(PDF_ROOT):
        print(f" '{PDF_ROOT}' folder not found.")
        return

    total_files = 0
    total_chunks = 0
    failed = []

    for sem_folder in sorted(os.listdir(PDF_ROOT)):
        sem_path = os.path.join(PDF_ROOT, sem_folder)

        if not os.path.isdir(sem_path):
            continue

        # Fix 1: handle both "sem4" and "SEM4"
        try:
            sem_num = int(sem_folder.upper().replace("SEM", ""))
        except:
            print(f"  Skipping '{sem_folder}' — name it SEM1, SEM2 etc.")
            continue

        print(f"\n Processing {sem_folder}/")

        # Fix 2: walk ALL subfolders recursively
        # os.walk goes through SEM4/AI/, SEM4/DAA/, SEM4/IT/ etc.
        for root, dirs, files in os.walk(sem_path):
            for filename in sorted(files):
                if not filename.endswith(".pdf"):
                    continue

                pdf_path = os.path.join(root, filename)

                # Get subject from the subfolder name
                # root = "pdfs/SEM4/AI" → subject = "AI"
                subject_folder = os.path.basename(root)
                if subject_folder.upper() == sem_folder.upper():
                    # PDF is directly in SEM folder, not in subject subfolder
                    subject = filename.replace(".pdf", "").title()
                else:
                    subject = subject_folder.title()

                print(f"   {subject}/{filename}")

                try:
                    result = parse_pdf(pdf_path)
                    chunks = chunk_by_pages(result)
                    embedded = embed_chunks(chunks)

                    metadata = {
                        "semester": sem_num,
                        "subject": subject,
                        "unit": None,
                        "doc_type": "notes",
                        "source_file": filename
                    }

                    store_chunks_with_metadata(embedded, metadata)

                    total_files += 1
                    total_chunks += len(embedded)
                    print(f"      {len(embedded)} chunks indexed")

                except Exception as e:
                    print(f"      Failed: {str(e)}")
                    failed.append(filename)

    print(f"\n{'='*40}")
    print(f" Ingestion complete!...")
    print(f"   Files indexed: {total_files}")
    print(f"   Total chunks: {total_chunks}")
    if failed:
        print(f"   Failed: {', '.join(failed)}")

if __name__ == "__main__":
    ingest_all()                        
