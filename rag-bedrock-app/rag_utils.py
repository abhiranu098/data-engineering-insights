import os
import json
import boto3
import numpy as np
import faiss
import pandas as pd
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# ---------- SAFE BEDROCK CLIENT ----------
def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )

# ---------- HELPERS ----------
def safe_text(text):
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="ignore")
    return str(text)

# ---------- FILE READERS ----------
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def read_csv(file):
    df = pd.read_csv(file)
    return df.to_string(index=False)

# ---------- CHUNKING ----------
def chunk_text(text, size=700, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# ---------- EMBEDDINGS ----------
def get_embedding(text):
    bedrock = get_bedrock_client()

    body = json.dumps({"inputText": safe_text(text)})

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=body
    )

    res = json.loads(response["body"].read().decode("utf-8"))
    return res["embedding"]

# ---------- VECTOR STORE ----------
def build_vector_store(chunks):
    embeddings = [get_embedding(c["chunk"]) for c in chunks]
    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index

# ---------- RETRIEVAL ----------
def retrieve(question, chunks, index, k=5):
    q_emb = np.array([get_embedding(question)], dtype="float32")
    _, indices = index.search(q_emb, k)
    return [chunks[i] for i in indices[0]]

# ---------- CLAUDE ----------
def ask_claude(question, context_chunks):
    bedrock = get_bedrock_client()

    context = "\n\n".join(
        [f"Source: {c['source']}\n{c['chunk']}" for c in context_chunks]
    )

    prompt = f"""
You are a knowledge assistant.
Answer ONLY using the provided context.
If the answer is not present, say:
"I don’t know based on the available information."

<context>
{context}
</context>

Question: {question}
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body
    )

    res = json.loads(response["body"].read().decode("utf-8"))
    return res["content"][0]["text"]
