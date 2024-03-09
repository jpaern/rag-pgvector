from dataclasses import dataclass
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    Text,
    create_engine,
    text,
)
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, declarative_base
from loguru import logger
from datetime import datetime
from openai import OpenAI
from pgvector.sqlalchemy import Vector

Base = declarative_base()


@dataclass
class TextEmbedding:
    text: str
    embedding: list[float]


class Embeddings(Base):
    __tablename__: str = "embeddings"
    id = Column(Integer(), primary_key=True)
    embedding = Column(Vector(3072))
    text = Column(Text)
    created_at = Column(DateTime(), default=datetime.now)


def get_url():
    url = URL.create(
        drivername="postgresql",
        username="testuser",
        host="localhost",
        database="vectordb",
    )
    return url


def activate_pgvector_extension(session):
    session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


def read_openai_token(filename: str = "auth_token.txt") -> str:
    with open(filename, "r") as f:
        token = f.read().strip()

    logger.info(f"token: <{token}>")
    return token


def get_openai_client(token: str) -> OpenAI:
    return OpenAI(api_key=token)


def get_embedding(
    texts: list[str], client: OpenAI, model: str = "text-embedding-3-large"
) -> list[float]:
    embeddings = []
    new_t = []
    for txt in texts:
        new_t.append(txt.replace("\n", " "))

    logger.info("Sending request to openai")
    res = client.embeddings.create(input=new_t, model=model)
    logger.info("  -> Received embeddings")
    for r in res.data:
        embeddings.append(r.embedding)

    return embeddings


if __name__ == "__main__":
    url = get_url()
    openai_token = read_openai_token()
    openai_client = get_openai_client(openai_token)
    texts = ["Juri ist der coolste", "Katzen habe Fell", "Aikido ist toll"]
    embeddings = get_embedding(texts, openai_client)

    ## DB

    logger.info(f"url: {url}")
    engine = create_engine(url)
    logger.info(f"engine: {engine}")
    with Session(engine) as session:
        activate_pgvector_extension(session)
    metadata = MetaData()
    metadata.create_all(engine)
    with Session(engine) as session:
        for e, t in zip(embeddings, texts):
            emb = Embeddings(embedding=e, text=t)
            session.add(emb)
        session.commit()
