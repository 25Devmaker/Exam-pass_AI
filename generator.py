from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

MODEL = "meta/llama-3.1-70b-instruct"


def find_images_for_pages(pages):
    # Placeholder implementation: return no images if there is no image lookup logic
    return []


def generate_answer(question, retrieved_chunks):
    context = ""
    pages_referenced = []

    for chunk in retrieved_chunks:
        context += f"\n[Source: Page {chunk['page']}]\n"
        context += chunk["text"]
        pages_referenced.append(chunk["page"])

    prompt = f"""You are ExamPass AI, an exam tutor for college students.
Answer the student's question using ONLY the context provided below.

Rules:
- If the question is simple (e.g. "what is X"), give a clear 2-3 line definition. Nothing more.
- If the question says "2 marks", answer in 2-3 short sentences like a student would write in an exam.
- If the question says "5 marks" or "explain in detail", give a structured detailed answer with points.
- If the question says "compare" or "difference", give a clear comparison between the concepts mentioned.
- If the question says "8 marks" or "10 marks", give a comprehensive answer with multiple points and examples.
- If the question says "list" or "enumerate", give bullet points only.
- answer only based on the programming and technology 
- Never add extra commentary, source references, or suggestions.
- If the answer is not in the context, use your own knowledge to answer clearly.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    try:
        # Streaming response with thinking enabled
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            top_p=0.95,
            max_tokens=4096,  # answer tokens
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 2048  # how much it thinks before answering
            },
            stream=True
        )

        answer = ""
        print("\nExamPass AI: ", end="", flush=True)

        for chunk in completion:
            if not chunk.choices:
                continue

            # Skip reasoning/thinking content — don't show it to student
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                continue  # model is thinking, don't print

            # Print and collect the actual answer
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                answer += content

        print()  # newline after streaming finishes

    except Exception as e:
        raise RuntimeError(f"Nvidia NIM error: {str(e)}")

    images = find_images_for_pages(list(set(pages_referenced)))

    return {
        "answer": answer,
        "pages": list(set(pages_referenced)),
        "images": images
    }
if __name__=="__main__":
    from retriever import retrieve

    print("===Exam Pass AI ===")
    print("type your questions (or 'quit' to exit )\n")

    while True:
        question = input("you: ").strip()

        if question.lower() == "quit":
            break
        if not question :
            continue
        print ("searching syllabus...")
        chunks= retrieve(question)

        print("generating answer...\n")
        result = generate_answer(question, chunks)

        print (f"exam pass Ai: {result['answer']}")

        print(f"\n Sources:pages {result['pages']}")

        if result["images"]:
            print(f"\n diagrams found:")
            for img in result["images"]:
                print(f"page {img['page']} -> {img['path']}")
        else:
            print("\n no diagrams found for this topic in your syllabus.")
        print("\n "+"="*40 + "\n") 