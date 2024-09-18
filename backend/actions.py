import httpx
import cohere
import requests
import google.generativeai as genai
import json
from fastapi import HTTPException
from config import Settings
from db.pinecone import PineconeManager

settings = Settings()
genai.configure(api_key=settings.google_api_key)
co_client=cohere.Client(api_key=settings.cohere_api_key)
pc = PineconeManager()
mailgun_domain_name=(settings.mail_gun_domain)

# book an appointment
def send_simple_message(question:str):
    try:
        print("SENT TO:",question)
        return requests.post(
            "https://api.mailgun.net/v3/sandboxbb2d48d0884645af91940da27085f932.mailgun.org/messages",
            auth=("api", settings.mail_gun_api_key),
            data={"from": "FinBOT <mailgun@sandboxbb2d48d0884645af91940da27085f932.mailgun.org>",
                "to": [question, "YOU@sandboxbb2d48d0884645af91940da27085f932.mailgun.org"],
                "subject": "Booking Successfull",
                "text": "This is a mock email for testing purpose only"})
    except Exception as e:
        return f"Error at smtp call: {str(e)}"
    

def book_appointment(question: str) -> str:
    """Use this function to book an appointment."""
    try:
        send_simple_message(question)
    except Exception as e:
        return f"Error: {str(e)}"  
    try:
        response = httpx.get('https://21bbs0122-bajaj-fullstack.vercel.app/book')
        response.raise_for_status()  
        response_json = response.json()
        message = response_json.get('message', 'No message found')  
        return message
    except Exception as e:
        return f"Error: {str(e)}"


# context fetcher
def answer_query(question: str):
    try:
        print("question to fetch: ",question)
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
            top_k=20,  # Adjust this number as needed
            include_metadata=True
        )
        #construct new prompt if match found and return prompt
        docs = {x["metadata"]['text']: i for i, x in enumerate(query_response["matches"])}

        rerank_docs = co_client.rerank(
            model="rerank-english-v3.0",
            query=question, 
            documents=list(docs.keys()), 
            top_n=5, 
            return_documents=True
        )
        # print("rerank_docs...",rerank_docs)

        # Extract reranked documents
        reranked_texts = [doc.document.text for doc in rerank_docs.results]
        # print("////////////////////////////////////////////RERANKED/////////////////////////////////")
        # print(reranked_texts)

        # contexts = []
        # for match in query_response['matches']:
        #     contexts.append(match['metadata']['text'])
        # if not contexts:
        #     return {"answer": "I found some matches, but they don't contain the expected metadata. Please check your document upload process."}
       
        prompt = f"""You are a helpful AI assistant. Use the following pieces of context to answer the user's question.In answer don't mentioned the context , don't say based on context provided. If the answer is not contained within the context, say "I don't have enough information to answer that question."
        Context:
        {' '.join(reranked_texts)}
        User's question: {question}
        """
        # print(prompt)
        return prompt
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")