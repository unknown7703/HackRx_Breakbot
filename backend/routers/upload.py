from fastapi import APIRouter, UploadFile, Depends, File
import os
import google.generativeai as genai
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import Settings
from db.pinecone import PineconeManager

# Loading environment variables
settings = Settings()
genai.configure(api_key=settings.google_api_key)

pc = PineconeManager()

router = APIRouter()

def process_pdf(file: UploadFile) -> List[str]:
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    
    loader = PyPDFLoader(temp_file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    texts = [str(doc) for doc in documents]
    
    os.remove(temp_file_path)
    
    return texts

def get_embeddings(texts: List[str]) -> List[List[float]]:
    embeddings_list = []
    for text in texts:
        result = genai.embed_content(
            model="models/embedding-001",  # TODO: Have to see which model is available at the moment
            content=text,
            task_type="retrieval_document",
            title="PDF Chunk Embedding"
        )
        embeddings_list.append(result['embedding'])
    return embeddings_list

@router.post("/upload")
async def upload_controller(file: UploadFile = File(...), pc: PineconeManager = Depends(PineconeManager)):
    if file.filename.endswith('.pdf'):
        texts = process_pdf(file)
        embeddings = get_embeddings(texts)
        
        ids = [f"{file.filename}_chunk_{i}" for i in range(len(texts))]
        
        pc.upsert_embeddings(pc.pinecone.Index(settings.pinecone_index), embeddings, ids, texts)
        
        return {
            "filename": file.filename,
            "chunks_processed": len(texts),
            "embedding_dimension": len(embeddings[0]),
            "first_5_values_of_first_embedding": embeddings[0][:5]
        }
    else:
        return {"error": "Please upload a PDF file"}
