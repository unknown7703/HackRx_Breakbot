from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from chat import post_chat_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str



@app.post("/chat")
async def post_query(request: QueryRequest):
    # Extract the query from the request body
    query_string = request.query
    response = post_chat_query(query_string)
    return {"bot_message": response}