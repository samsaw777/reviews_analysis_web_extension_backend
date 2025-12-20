from fastapi import APIRouter, HTTPException, Body
import json
from core.basic_chain import ask_question

router = APIRouter()


@router.post("/get_review_summary")
async def get_review_summary(raw_body: str = Body(...)):
    try:
        # 1️⃣ Parse the raw JSON.stringify body
        parsed_data = json.loads(raw_body)

        # 2️⃣ Extract product info
        product_name = parsed_data.get("productName", "")
        product_price = parsed_data.get("productPrice", "")
        product_rating = parsed_data.get("productRating", "")

        # 3️⃣ Extract reviews array
        reviews_list = parsed_data.get("reviews", [])

        if not reviews_list:
            raise ValueError("No reviews found in request body")

        # 4️⃣ Extract review text
        review_texts = [review["body"] for review in reviews_list]

        # 5️⃣ Convert List[str] → single string
        formatted_reviews = "\n".join(
            [f"{i+1}. {text}" for i, text in enumerate(review_texts)]
        )

        # 6️⃣ Run sentiment analysis
        analysis = ask_question(
            product_name=product_name,
            product_price=product_price,
            product_rating=product_rating,
            reviews=formatted_reviews
        )

        return {
            "success": True,
            "message": "Sentiment analysis completed",
            "data": analysis
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON.stringify body")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
