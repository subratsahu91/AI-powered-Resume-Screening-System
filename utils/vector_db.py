import chromadb
from chromadb.config import Settings

_chroma_client = None  # 👈 global singleton


def get_chroma_client(persist_dir=None):
    global _chroma_client

    if _chroma_client is None:
        if persist_dir:
            _chroma_client = chromadb.Client(
                Settings(
                    persist_directory=persist_dir,
                    anonymized_telemetry=False,
                )
            )
        else:
            _chroma_client = chromadb.Client(
                Settings(
                    anonymized_telemetry=False,
                )
            )

    return _chroma_client


def get_collection(name, persist_dir=None):
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name)
