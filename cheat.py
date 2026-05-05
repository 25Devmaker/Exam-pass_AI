from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(); client = OpenAI()

vs_id:"vs_69f390ffe50c8191be2179dd9540b36a"
def ask(q):
    r =client.response.create(
        input=q,
        model="gpt-4o-mini",
        tools=[{"type":"file_search","vector_store_ids":[vs_id]}]
    )

    return r.output[-1].context[0].text
print(f"what is AI?")    


