import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from phi.assistant import Assistant, AssistantMemory
from phi.llm.groq import Groq
from actions import book_appointment
from actions import cancel_appointment

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

def prompt_Controller(question: str):
    try:
        question_embedding = genai.embed_content(
            model="models/embedding-001",
            content=question,
            task_type="retrieval_document",
            title="Question Embedding"
        )['embedding']

        query_response = pc.pinecone.Index(settings.pinecone_index).query(
            vector=question_embedding,
            top_k=5,  # Adjust this number as needed
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

    User's question: {question}

    Your answer:"""

        # response = groq_client.chat.completions.create(
        #     model="llama3-8b-8192",  # You can change this to the appropriate Groq model
        #     messages=[
        #         {"role": "system", "content": "You are a helpful AI assistant."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.2,
        #     max_tokens=1024,
        # )

        return prompt

    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

class ResponseStructure(BaseModel):
    message:str = Field(..., description="Provide the answer from llm. Don't provide markdown, only provide the answer camelCase")

ASSISTANT_DESCRIPTION = """
    You are a helpful AI assistant that is being used by Bajaj Finserv. Bajaj Finserv is a financial services company based out of India. They mostly deal with various types of insurance, such as health, vehicle, travel, home, etc.

    INSTRUCTIONS:
    1. Answer questions only using the context that is provided.
    2. Use the tools that are available whenever you require.
    3. If you don't have ample information then respond - I am sorry. I don't have enough information to answer that question.
    4. If any words are present in all caps, return then in lower case.
    5. ALWAYS provide the answer in JSON.
"""

#Assitant
assistant=Assistant(
    llm=Groq(model="llama3-8b-8192"),
    description=ASSISTANT_DESCRIPTION,
    instructions=[
        "Use the book_appointment function to book an appointment when the user will ask",
        "Use the cancel_appointment function to cancel an appointment when the user will ask",
    ],
    # tools=[book_appointment, cancel_appointment],
    # show_tool_calls=True,
    output_model=ResponseStructure,
    debug_mode=True,
    read_chat_history=True,
    markdown=False
)

@router.post("/chat")
def assistant_caller(question: QuestionModel):
    try:
        question_string=question.text
        final_context=prompt_Controller(question_string)
        response=assistant.run(final_context)
        memory: AssistantMemory = assistant.memory
        return {"message":response}
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


