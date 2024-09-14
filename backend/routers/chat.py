import json
import logging

from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

from actions import book_appointment, answer_query
from config import Settings

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

settings = Settings()
client = Groq(api_key=settings.GROQ_API_KEY)

router = APIRouter()

class QuestionModel(BaseModel):
    text: str

def prompt_Controller(user_prompt):
    logger.info("Starting prompt controller")
    start_time = datetime.now()

    messages = [
        {
            "role": "system",
            "content": "You are a good assistant , you use answer query tool to answer question , do not answer question/query on your own ever, only use tool to answer. If requested specifically to book appointment you can use book appointment tool to do so , only reply the returning message from the tool call do not add any of your own answer"
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
    
    logger.info("Making chat completion request")
    response_start = datetime.now()
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
        max_tokens=1024
    )
    response_end = datetime.now()
    logger.info(f"Chat completion request took {(response_end - response_start).total_seconds()} seconds")
    
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
            logger.info(f"Calling tool: {function_name}")
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            logger.info(f"Arguments for {function_name}: {function_args}")

            tool_call_start = datetime.now()
            function_response = function_to_call(
                question=function_args.get("question")
            )
            tool_call_end = datetime.now()
            logger.info(f"Tool {function_name} completed in {(tool_call_end - tool_call_start).total_seconds()} seconds")
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        logger.info("Making second chat completion request")
        second_response_start = datetime.now()
        second_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        second_response_end = datetime.now()
        logger.info(f"Second chat completion request took {(second_response_end - second_response_start).total_seconds()} seconds")
        
        return {"message": second_response.choices[0].message.content}

    end_time = datetime.now()
    logger.info(f"Prompt controller finished in {(end_time - start_time).total_seconds()} seconds")

@router.post("/ask")
def assistant_caller(question: QuestionModel):
    try:
        logger.info(f"Received question: {question.text}")
        question_string = question.text
        response = prompt_Controller(question)
        logger.info("Question processed successfully")
        return {"message": response}
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
