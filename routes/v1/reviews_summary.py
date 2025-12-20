from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from core.basic_chain import ask_question

router = APIRouter()


@router.post("/get_review_summary")
async def get_review_summary(payload: Dict[str, Any]):
    try:
        # 1️⃣ Extract product info
        product_name = payload.get("productName", "")
        product_price = payload.get("productPrice", "")
        product_rating = payload.get("productRating", "")

        # 2️⃣ Extract reviews
        reviews_list = payload.get("reviews", [])
        if not reviews_list:
            raise ValueError("No reviews provided")

        # 3️⃣ Extract review text
        review_texts = [r.get("body", "") for r in reviews_list]

        formatted_reviews = "\n".join(
            [f"{i+1}. {text}" for i, text in enumerate(review_texts)]
        )

        # 4️⃣ Call LLM chain
        analysis = ask_question(
            product_name=product_name,
            product_price=product_price,
            product_rating=product_rating,
            reviews=formatted_reviews
        )

        # 5️⃣ Compute numeric sentiment score in Python
        ratings = [r.get("rating", 0) for r in reviews_list if "rating" in r]
        if ratings:
            analysis["sentiment_score"] = round(sum(ratings) / len(ratings), 1)
        else:
            analysis["sentiment_score"] = None

        return {
            "success": True,
            "message": "Sentiment analysis completed",
            "data": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
