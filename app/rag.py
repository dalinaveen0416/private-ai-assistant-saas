import os

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_groq import ChatGroq

from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()
prompt_template = PromptTemplate(

    input_variables=["context", "question"],

    template="""
You are a professional AI Resume Assistant.

Your job is to answer questions ONLY using the provided resume context.

RULES:

1. Answer strictly from the resume context.
2. Do NOT make up information.
3. If answer is not present, say:
   "The information is not available in the resume."
4. Keep answers clear and professional.
5. Give short and precise answers.
6. If question asks about:

   - Name ->return full name
   - Skills -> list skills
   - Experience -> summarize experience
   - Projects -> explain briefly
   - Education -> give degree and college

7. Never mention "context" or "document" in answer.

RESUME CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""
)



def ask_question(user_id, query):

    embeddings = HuggingFaceEmbeddings()

    db = FAISS.load_local(

        f"vectorstore/{user_id}",

        embeddings,

        allow_dangerous_deserialization=True
    )


    retriever = db.as_retriever()


    llm = ChatGroq(

        api_key=os.getenv("GROQ_API_KEY"),

        model="llama-3.3-70b-versatile",
        prompt=prompt_template
    )


    qa = RetrievalQA.from_chain_type(

        llm=llm,

        retriever=retriever
    )


    return qa.run(query)
