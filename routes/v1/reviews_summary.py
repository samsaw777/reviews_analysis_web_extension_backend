from fastapi import APIRouter, HTTPException
from typing import Optional,List, Dict, Any
from pydantic import BaseModel
from core.basic_chain import ask_question
import json

router = APIRouter()

class ReviewItem(BaseModel):
    id: int
    rating: int
    title: str
    body: str
    author: str
    date: str
    isVerified: bool
    helpfulVotes: int


class ReviewRequest(BaseModel):
    success: bool
    productName: str
    productRating: str
    totalReviewCount: str
    reviews: List[ReviewItem]
    totalReviews: int
    scrapedAt: str

@router.post("/get_review_summary")
async def get_review_summary(payload: ReviewRequest):
    try:
  
        # print(user_input)
        review_texts = [review.body for review in payload.reviews]
        
        # format the reviews
        formatted_reviews = "\n".join(
            [f"{i+1}. {text}" for i, text in enumerate(review_texts)]
        )
        response = ask_question(formatted_reviews)    
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

