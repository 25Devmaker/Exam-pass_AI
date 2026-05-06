---
title: Devnexusbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---
# 🎓 ExamPass AI

> Ask your exam question. Get your exam answer. That's it.

ExamPass AI is a RAG-based AI assistant that reads your actual semester PDFs and answers your exam questions in the exact format your professor expects.

**Built by:** [25Devmaker](https://github.com/25Devmaker) — BCA 2nd Year, Bengaluru

---

## 🤖 Try it on Telegram

**[@TaskNucleusBot](https://t.me/TaskNucleusBot)**

No login. No app download. Just open the bot and ask your question.

---

## 💡 How to Use

Just type your question the way you'd write it in your exam:

```
explain artificial intelligence in 2 marks
what is machine learning in 5 marks
explain neural networks in 10 marks
```

The bot reads your question, finds the most relevant content from your syllabus, and generates an answer in the exact mark format you asked for.

---

## 🧠 How It Works

```
Semester PDFs
     ↓
parser.py        →  extracts raw text from PDFs (PyMuPDF)
     ↓
chunker.py       →  splits into 500-word chunks, 50-word overlap
     ↓
embedder.py      →  converts chunks to 768-dim vectors (CodeBERT)
     ↓
ChromaDB         →  stores vectors locally, persistent
     ↓
retriever.py     →  finds most relevant chunks via cosine similarity
     ↓
generator.py     →  Llama 3.1 70B generates answer via Nvidia NIM
     ↓
telegram_bot.py  →  sends answer to student on Telegram
```

---

## 📚 Subjects Covered

| Semester | Subject | Status |
|----------|---------|--------|
| SEM4 | Artificial Intelligence | ✅ Live |
| SEM1-SEM6 | More subjects | 🔄 Adding soon |

> Want your subject added? Drop a comment or message the bot.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| PDF Parsing | PyMuPDF |
| Embeddings | microsoft/codebert-base (768-dim) |
| Vector DB | ChromaDB (local, persistent) |
| LLM | Nvidia NIM — meta/llama-3.1-70b-instruct |
| Bot | python-telegram-bot |
| Deployment | Railway |

---

## 📁 Project Structure

```
exampass-ai/
│
├── parser.py         # Extracts text from PDFs
├── chunker.py        # Splits text into overlapping chunks
├── embedder.py       # Generates embeddings using CodeBERT
├── retriever.py      # Retrieves relevant chunks from ChromaDB
├── generator.py      # Generates answers using Nvidia NIM
├── ingestor.py       # Walks SEM1-SEM6 folders, indexes all PDFs
├── main.py           # CLI interface for testing
├── bot.py   # Telegram bot interface
├── requirements.txt
└── .env              # API keys (never committed)
```

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/25Devmaker/Exam-pass_AI.git
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
# Add your API keys
```

**4. Add your PDFs**
```
data/
├── SEM1/subject-name/file.pdf
├── SEM4/AI/module1.pdf
```

**5. Ingest PDFs**
```bash
python ingestor.py
```

**6. Run the bot**
```bash
python telegram_bot.py
```

---

## 🔑 Environment Variables

```env
NVIDIA_API_KEY=your_nvidia_nim_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

---

## 📌 Why I Built This

Every student before exams is in panic mode — scrambling through 200 pages of PDFs, WhatsApp notes, random YouTube videos.

I wanted one place where you just ask and get the answer in your exact exam format. No hallucinations. No random internet answers. Only answers from your actual syllabus.

---

## 🗺️ Roadmap

- [x] RAG pipeline from scratch
- [x] Multi-semester folder support
- [x] Telegram bot with streaming
- [ ] Railway deployment
- [ ] SEM1-SEM6 full coverage
- [ ] Filter by subject and unit
- [ ] Web interface

---

## 👨‍💻 Author

**25Devmaker**
- GitHub: [@25Devmaker](https://github.com/25Devmaker)
- LinkedIn: [Build in Public](linkedin.com/in/hari-kishan-devmaker)

---

*Built from scratch. No frameworks. Just Python and curiosity.*