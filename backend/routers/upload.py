import os
import logging
from typing import List
from datetime import datetime
import google.generativeai as genai
from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.auto import partition

from config import Settings
from db.pinecone import PineconeManager

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

settings = Settings()
genai.configure(api_key=settings.GOOGLE_API_KEY)
pc = PineconeManager()

router = APIRouter()

class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

def process_file(file: UploadFile) -> List[str]:
    logger.info(f"Starting file processing: {file.filename}")
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    
    start_partition_time = datetime.now()
    logger.info(f"Partitioning file: {file.filename}")
    elements = partition(temp_file_path)
    end_partition_time = datetime.now()
    logger.info(f"Partitioning completed for {file.filename} in {(end_partition_time - start_partition_time).total_seconds()} seconds")
    
    documents_list = [Document(page_content=element.text, metadata={}) for element in elements]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_start_time = datetime.now()
    logger.info(f"Splitting text for {file.filename}")
    split_documents = text_splitter.split_documents(documents_list)
    split_end_time = datetime.now()
    logger.info(f"Text splitting completed for {file.filename} in {(split_end_time - split_start_time).total_seconds()} seconds")
    
    texts = [doc.page_content for doc in split_documents]
    
    os.remove(temp_file_path)
    logger.info(f"Temp file removed: {temp_file_path}")
    
    return texts

def get_embeddings(texts: List[str]) -> List[List[float]]:
    embeddings_list = []
    for i, text in enumerate(texts):
        start_embedding_time = datetime.now()
        logger.info(f"Generating embedding for chunk {i}")
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document",
            title="Document Chunk Embedding"
        )
        embeddings_list.append(result['embedding'])
        end_embedding_time = datetime.now()
        logger.info(f"Embedding generated for chunk {i} in {(end_embedding_time - start_embedding_time).total_seconds()} seconds")
    return embeddings_list

ALLOWED_EXTENSIONS = ('.pdf', '.doc', '.docx', '.ppt', '.pptx')

@router.post("/upload")
async def upload_controller(
    files: List[UploadFile] = File(...),
    pc: PineconeManager = Depends(PineconeManager)
):
    start_time = datetime.now()
    logger.info(f"Upload process started at {start_time}")
    
    all_texts = []
    all_embeddings = []
    all_ids = []

    for file in files:
        file_start_time = datetime.now()
        logger.info(f"Processing file: {file.filename}")
        
        if not file.filename.endswith(ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file.filename}")
        
        texts = process_file(file)
        all_texts.extend(texts)

        embeddings = get_embeddings(texts)
        all_embeddings.extend(embeddings)

        ids = [f"{file.filename}_chunk_{i}" for i in range(len(texts))]
        all_ids.extend(ids)
        
        file_end_time = datetime.now()
        logger.info(f"Finished processing {file.filename} in {(file_end_time - file_start_time).total_seconds()} seconds")

    upsert_start_time = datetime.now()
    logger.info("Upserting embeddings to Pinecone")
    
    pc.upsert_embeddings(pc.pinecone.Index(settings.PINECONE_INDEX), all_embeddings, all_ids, all_texts)

    upsert_end_time = datetime.now()
    logger.info(f"Upserting completed in {(upsert_end_time - upsert_start_time).total_seconds()} seconds")

    end_time = datetime.now()
    logger.info(f"Upload process completed at {end_time}")
    logger.info(f"Total time taken: {(end_time - start_time).total_seconds()} seconds")

    return {
        "files_processed": len(files),
        "chunks_processed": len(all_texts),
        "embedding_dimension": len(all_embeddings[0]),
        "first_5_values_of_first_embedding": all_embeddings[0][:5]
    }
