from fastapi import APIRouter, UploadFile, Depends

from sqlalchemy.orm import Session
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.database import get_db
from app.models import Document
from app.deps import get_user


from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


router = APIRouter()


@router.post("/upload")
def upload(
    file: UploadFile,
    user_id: int = Depends(get_user),
    db: Session = Depends(get_db)
):

    # create folder
    os.makedirs("uploads", exist_ok=True)


    filepath = f"uploads/{user_id}.pdf"


    # save file
    with open(filepath, "wb") as f:

        f.write(file.file.read())


    # load PDF
    loader = PyPDFLoader(filepath)

    docs = loader.load()


    # embeddings
    embeddings = HuggingFaceEmbeddings()


    # vector store path
    vector_path = f"vectorstore/{user_id}"


    db_faiss = FAISS.from_documents(
        docs,
        embeddings
    )


    db_faiss.save_local(vector_path)


    # save in MySQL
    document = Document(

        user_id=user_id,

        filename=file.filename,

        vector_path=vector_path
    )


    db.add(document)

    db.commit()


    return {

        "message": "PDF uploaded successfully"
    }
