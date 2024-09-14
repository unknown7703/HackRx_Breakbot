import httpx
import logging

import google.generativeai as genai
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel
from groq import Groq

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
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def book_appointment(question: str) -> str:
    """Use this function to book an appointment."""
    try:
        logger.info("Starting book_appointment function")
        start_time = datetime.now()

        response = httpx.get('https://21bbs0122-bajaj-fullstack.vercel.app/book')
        response.raise_for_status()

        response_json = response.json()
        message = response_json.get('message', 'No message found')

        end_time = datetime.now()
        logger.info(f"book_appointment function finished in {(end_time - start_time).total_seconds()} seconds")

        return message

    except Exception as e:
        logger.error(f"Error in book_appointment: {str(e)}")
        return f"Error: {str(e)}"

def answer_query(question: str):
    try:
        logger.info("Starting answer_query function")
        start_time = datetime.now()

        embedding_start = datetime.now()
        question_embedding = genai.embed_content(
            model="models/embedding-001",
            content=question,
            task_type="retrieval_document",
            title="Question Embedding"
        )['embedding']
        embedding_end = datetime.now()
        logger.info(f"Question embedding generated in {(embedding_end - embedding_start).total_seconds()} seconds")

        query_start = datetime.now()
        query_response = pc.pinecone.Index(settings.PINECONE_INDEX).query(
            vector=question_embedding,
            top_k=10,
            include_metadata=True
        )
        query_end = datetime.now()
        logger.info(f"Pinecone query finished in {(query_end - query_start).total_seconds()} seconds")

        contexts = []
        for match in query_response['matches']:
            contexts.append(match['metadata']['text'])

        if not contexts:
            logger.warning("No contexts found in Pinecone matches")
            return {"answer": "I found some matches, but they don't contain the expected metadata. Please check your document upload process."}

        prompt = f"""
        You are a helpful AI assistant. Use the following pieces of context to answer the user's question. In answer don't mention the context, don't say based on context provided. If the answer is not contained within the context, say "I don't have enough information to answer that question."

        CONTEXT:
        {' '.join(contexts)}

        USER's QUESTION: 
        {question}
        """

        end_time = datetime.now()
        logger.info(f"answer_query function finished in {(end_time - start_time).total_seconds()} seconds")

        return prompt

    except Exception as e:
        logger.error(f"Error in answer_query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
