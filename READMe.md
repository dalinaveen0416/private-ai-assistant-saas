# Private AI Assistant SaaS (Multi-User, RAG, FastAPI, MySQL, Groq)

This project is a full-stack AI SaaS platform where users can register, upload their own documents, and chat with a private AI assistant that answers based on their uploaded files.

Each user has their own data, chat history, and vector database. The system is built using FastAPI for the backend, MySQL for database, FAISS for vector search, Groq LLM for AI responses, and Streamlit for the frontend.

I built this project to simulate how real AI SaaS products work in production.

---

# What this project can do

• User registration and login
• JWT authentication
• Upload multiple PDF documents
• Chat with AI based on uploaded documents
• Store chat history
• Track usage
• Multi-user support
• ChatGPT-style UI

Each user’s data is completely isolated.

---

# Tech Stack

Python
FastAPI
MySQL
SQLAlchemy
Streamlit
LangChain
FAISS
Groq LLM
JWT Authentication

---

# Project Structure

```
private_ai_assistant_saas/

├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── deps.py
│   ├── rag.py
│   └── routes/
│        ├── auth_routes.py
│        ├── upload_routes.py
│        ├── chat_routes.py
│        └── history_routes.py
|
├── vectorstore/
├── uploads/
├── user_interface.py
├── schema.sql
├── requirements.txt
└── README.md
```

---

# Step 1 — Clone project

```
git clone <your repo url>

cd private_ai_assistant_saas
```

---

# Step 2 — Create virtual environment

Windows:

```
python -m venv env

env\Scripts\activate
```

Mac/Linux:

```
python3 -m venv env

source env/bin/activate
```

---

# Step 3 — Install requirements

```
pip install -r requirements.txt
``` 

---

# Step 4 — MySQL setup

Make sure MySQL is installed and running.

MySQL credentials used in this project:

```
User: username
Password: Password
Host: 127.0.0.1 HOST NAME
Port: 3306
Database: DATABASE NAME
```

Login to MySQL:

```
mysql -u root -p
```

Enter password:

```
your password
```

Run schema:

```
source schema.sql;
```

Or

```
mysql -u root -p DB_Name < schema.sql
```

---

# Step 5 — Create .env file

Create a file named:

```
.env
```

Add:

```
GROQ_API_KEY=your_groq_api_key

```

You can get Groq key from:

https://console.groq.com/

---

# Step 6 — Run FastAPI backend

From project root:

```
uvicorn app.main:app --reload --port 9000
```

Backend will run at:

```
http://127.0.0.1:9000
```

API docs:

```
http://127.0.0.1:9000/docs
```

---

# Step 7 — Run Streamlit frontend

Open new terminal

Activate environment

Run:

```
streamlit run streamlit.py
```

Streamlit runs at:

```
http://localhost:8501
```

---

# Step 8 — How to use

Register account

Login

Upload resume PDF

Go to chat

Ask questions like:

```
What is my name?

What are my skills?

What projects do I have?
```

AI will answer based on your document.

---

# How it works internally

User uploads PDF

↓

Text converted to embeddings

↓

Stored in FAISS vector database

↓

User asks question

↓

Relevant content retrieved

↓

Sent to Groq LLM

↓

Response generated

↓

Saved in MySQL

---

# Database Tables

users

documents

chat_history

usage_tracking

---

# Example Chat

User:

What is my name?

AI:

Your name is Naveen Dali.

---

# Port Information

FastAPI:

9000

Streamlit:

8501

MySQL:

3306

---

# Requirements

Python 3.10 recommended

MySQL installed

Groq API key

---

# requirements.txt

```
fastapi
uvicorn
sqlalchemy
pymysql
passlib
python-jose
langchain
langchain-community
langchain-groq
sentence-transformers
faiss-cpu
streamlit
python-dotenv
```

---

# Why I built this

I wanted to understand how real AI SaaS systems work, including authentication, vector databases, and multi-user architecture.

This project helped me learn backend development, AI integration, and production-level design.

---

# Author

Naveen Dali

Python Developer
Generative AI Engineer

---
