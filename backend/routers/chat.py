import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from groq import Groq
from actions import book_appointment
from actions import answer_query
from config import Settings


# Loading environment variables
settings = Settings()
client = Groq(api_key=settings.groq_api_key)

router = APIRouter()

class QuestionModel(BaseModel):
    query: str

# main llm caller with subcalling 
def prompt_Controller(user_prompt):
    messages=[
        {
            "role": "system",
            "content": "You are a good assistant , you use answer query tool to answer question , do not answer question/query on your own ever, only use tool to answer. If requested specifiaclly to book appointment you can use book appointment tool to do so , only reply the returning message from the tool call do not add any of your own answer"
        },
        {
            "role": "user",
            "content": user_prompt.query,
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
    # first llm call to decide further actions needed to be performed eg. retirval, api call etc
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
        #for each tool call append message with relevant tool detail
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                question=function_args.get("question")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        # second llm call based on newly constructed message   
        second_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return second_response.choices[0].message.content

@router.post("/chat")
def assistant_caller(question: QuestionModel):
    try:
        question_string=question.query
        response=prompt_Controller(question)
        return {"bot_message":response}
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")