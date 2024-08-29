import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

from config import Settings
from db.pinecone import PineconeManager

# Loading environment variables
settings = Settings()
genai.configure(api_key=settings.google_api_key)

pc = PineconeManager()
groq_client = Groq(api_key=settings.groq_api_key)

router = APIRouter()

class QuestionModel(BaseModel):
    text: str

@router.post("/chat")
def prompt_Controller(question: QuestionModel):
    try:
        question_embedding = genai.embed_content(
            model="models/embedding-001",
            content=question.text,
            task_type="retrieval_document",
            title="Question Embedding"
        )['embedding']

        query_response = pc.pinecone.Index(settings.pinecone_index).query(
            vector=question_embedding,
            top_k=10,  # Adjust this number as needed
            include_metadata=True
        )

        print(query_response)

        # if not query_response['matches']:
        #     return {"answer": "I'm sorry, but I don't have enough information to answer that question. Please make sure you've uploaded relevant documents first."}

        contexts = []
        for match in query_response['matches']:
            contexts.append(match['metadata']['text'])
        # else:
        #     print(f"Unexpected match structure: {match}")  # For debugging

        print("Context :" + str(contexts))

        if not contexts:
            return {"answer": "I found some matches, but they don't contain the expected metadata. Please check your document upload process."}

        # Construct the prompt for the LLM
        prompt = f"""You are a helpful AI assistant. Use the following pieces of context to answer the user's question. If the answer is not contained within the context, say "I don't have enough information to answer that question."

    Context:
    {' '.join(contexts)}

    User's question: {question.text}

    Your answer:"""

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # You can change this to the appropriate Groq model
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024,
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")