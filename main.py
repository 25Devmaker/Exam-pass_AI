# main.py
import os
from retriever import retrieve
from generator import generate_answer

print("=== ExamPass AI ===\n")

# Safety check — warn if nothing is indexed yet
if not os.path.exists("chroma_db"):
    print(" No syllabus indexed yet. Run: python ingestor.py first")
    exit()

while True:
    question = input("\nYou: ").strip()

    if question.lower() in ["quit", "exit"]:
        break
    if not question:
        continue

    chunks = retrieve(question)
    result = generate_answer(question, chunks)

    print(f"\n Sources:Pages {result['pages']}")
    if result["images"]:
        for img in result["images"]:
            print(f"Diagram -> {img['path']}")