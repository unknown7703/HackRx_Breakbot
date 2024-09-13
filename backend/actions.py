import httpx
import google.generativeai as genai
import json
from fastapi import HTTPException
from config import Settings
from db.pinecone import PineconeManager

settings = Settings()
genai.configure(api_key=settings.google_api_key)
pc = PineconeManager()


# book an appointment
def book_appointment(question: str) -> str:
    """Use this function to book an appointment."""
    try:
        # Call API for booking
        response = httpx.get('https://21bbs0122-bajaj-fullstack.vercel.app/book')
        response.raise_for_status()  # Ensure we raise an exception for HTTP errors

        # Load JSON from the response
        response_json = response.json()

        # Extract the message or other content from the JSON response
        message = response_json.get('message', 'No message found')  # Adjust key as needed

        return message

    except Exception as e:
        # Log the exception if needed, here we just return an error message
        return f"Error: {str(e)}"


# context fetcher
def answer_query(question: str):
    try:
        # make vector embedding of the question
        question_embedding = genai.embed_content(
            model="models/embedding-001",
            content=question,
            task_type="retrieval_document",
            title="Question Embedding"
        )['embedding']
        # fetch semantic search by matching question embedding with existing chunks from document
        query_response = pc.pinecone.Index(settings.pinecone_index).query(
            vector=question_embedding,
            top_k=10,  # Adjust this number as needed
            include_metadata=True
        )
        #construct new prompt if match found and return prompt
        contexts = []
        for match in query_response['matches']:
            contexts.append(match['metadata']['text'])
        if not contexts:
            return {"answer": "I found some matches, but they don't contain the expected metadata. Please check your document upload process."}
       
        prompt = f"""You are a helpful AI assistant. Use the following pieces of context to answer the user's question.In answer don't mentioned the context , don't say based on context provided. If the answer is not contained within the context, say "I don't have enough information to answer that question."
        Context:
        {' '.join(contexts)}
        User's question: {question}
        Your answer:"""
        return prompt
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")