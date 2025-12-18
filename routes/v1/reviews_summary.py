from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from core.basic_chain import ask_question

router = APIRouter()

class Review(BaseModel):
    question:str

@router.post("/get_review_summary")
async def get_review_summary(user_input:Review):
    response = ask_question(user_input.question)

    return response