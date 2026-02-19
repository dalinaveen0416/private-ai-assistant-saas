from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String(255), unique=True)

    password = Column(String(255))

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    filename = Column(String(255))

    vector_path = Column(String(255))

    uploaded_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    query = Column(Text)

    response = Column(Text)

    tokens_used = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


class UsageTracking(Base):

    __tablename__ = "usage_tracking"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, unique=True)

    query_count = Column(Integer)

    token_usage = Column(Integer)

    last_updated = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
