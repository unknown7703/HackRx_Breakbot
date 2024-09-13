import google.generativeai as genai
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from groq import Groq
from actions import book_appointment
from actions import answer_query

from config import Settings
from db.pinecone import PineconeManager

# Loading environment variables
settings = Settings()
client = Groq(api_key=settings.groq_api_key)

router = APIRouter()

class QuestionModel(BaseModel):
    text: str

def prompt_Controller(user_prompt):
    messages=[
        {
            "role": "system",
            "content": "You are a good assistant , you use answer query tool to answer question , do not answer question/query on your own ever, only use tool to answer. If requested specifiaclly to book appointment you can use book appointment tool to do so , only reply the returning message from the tool call do not add any of your own answer"
        },
        {
            "role": "user",
            "content": user_prompt.text,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "book_appointment",
                "description": "Book an appointment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The type of appointment",
                        }
                    },
                    "required": ["question"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "answer_query",
                "description": "answer query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "question/query asked by user",
                        }
                    },
                    "required": ["question"],
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
        max_tokens=1024
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        
        available_functions = {
            "book_appointment": book_appointment,
            "answer_query": answer_query,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            print("function_name",function_name)
            function_to_call = available_functions[function_name]
            print("function_to_call",function_to_call)
            function_args = json.loads(tool_call.function.arguments)
            print("function_args",function_args)

            function_response = function_to_call(
                question=function_args.get("question")
            )
            
            
            print("function_response",function_response)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return {"message":second_response.choices[0].message.content}

@router.post("/chat")
def assistant_caller(question: QuestionModel):
    try:
        question_string=question.text
        response=prompt_Controller(question)
        return {"message":response}
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")






















 

        #print(query_response)

        # if not query_response['matches']:
        #     return {"answer": "I'm sorry, but I don't have enough information to answer that question. Please make sure you've uploaded relevant documents first."}

        
        # else:
        #     print(f"Unexpected match structure: {match}")  # For debugging

        #print("Context :" + str(contexts))

        
        # Construct the prompt for the LLM
        # prompt = f"""You are a helpful AI assistant. Use the following pieces of context to answer the user's question.In answer don't mentioned the context , don't say based on context provided. If the answer is not contained within the context, say "I don't have enough information to answer that question."
        # Context:
        # {' '.join(contexts)}
        # User's question: {question}
        # Your answer:"""