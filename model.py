import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import logging
import sys
import config

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    PromptTemplate,
)
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


global query_engine
query_engine = None


def init_llm():
    llm = Ollama(model="llama2:7b", request_timeout=30.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model


def init_index(embed_model):
    reader = SimpleDirectoryReader(input_dir=config.DOCS_DIR, recursive=True)
    documents = reader.load_data()

    logging.info("index creating with `%d` documents", len(documents))

    chroma_client = chromadb.HttpClient(
        config.CHROMA_HOST,
        config.CHROMA_PORT,
        ssl=False,
        headers=None,
        # settings=Settings,
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    chroma_collection = chroma_client.get_or_create_collection("rag")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # use this to set custom chunk size and splitting
    # https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=Settings.embed_model
    )

    return index


def init_query_engine(index):
    global query_engine

    # custome prompt template
    template = (
        "Jesteś zaawansowanym asystentem AI, wyspecjalizowanym w pomaganiu studentom na podstawie materiałów z uczelni. "
        "Masz dostęp do różnych dokumentów akademickich, takich jak zadania, notatki z wykładów, prezentacje, fragmenty kodu oraz pliki projektowe.\n\n"
        "Oto kontekst wyciągnięty z dostępnych materiałów:\n"
        "-----------------------------------------\n"
        "{context_str}\n"
        "-----------------------------------------\n"
        "Na podstawie powyższych informacji odpowiedz na poniższe pytanie jak najdokładniej i jak najjaśniej. "
        "Jeśli to możliwe, odwołaj się do konkretnych tematów lub materiałów z kursów.\n\n"
        "Pytanie: {query_str}\n\n"
        "Udziel pomocnej, zwięzłej i zrozumiałej odpowiedzi, odpowiedniej dla studenta."
    )

    qa_template = PromptTemplate(template)

    # build query engine with custom template
    # text_qa_template specifies custom template
    # similarity_top_k configure the retriever to return the top 3 most similar documents,
    # the default value of similarity_top_k is 2
    query_engine = index.as_query_engine(
        text_qa_template=qa_template, similarity_top_k=3
    )

    return query_engine


def chat(input_question):
    global query_engine

    response = query_engine.query(input_question)
    logging.info("got response from llm - %s", response)

    return response.response


def chat_cmd():
    global query_engine

    while True:
        input_question = input("Enter your question (or 'exit' to quit): ")
        if input_question.lower() == "exit":
            break

        response = query_engine.query(input_question)
        logging.info("got response from llm - %s", response)


if __name__ == "__main__":
    init_llm()
    index = init_index(Settings.embed_model)
    init_query_engine(index)
    chat_cmd()
