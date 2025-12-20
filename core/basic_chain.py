# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# import json

# load_dotenv()

# JSON_SCHEMA = r"""
# {
#   "overall_sentiment": "positive | mixed | negative",
#   "sentiment_score": 0.0,
#   "risk_level": "low | medium | high",
#   "deal_breakers": ["string"],
#   "most_common_complaints": ["string"],
#   "who_should_avoid": "string",
#   "summary": "string"
# }
# """

# def ask_question(reviews: str) -> dict:
#     prompt = PromptTemplate.from_template(
#         """
#             You are an unbiased product review analyst.

#             IMPORTANT:
#             - Do NOT assume the product is good just because reviews are mostly positive.
#             - Actively look for complaints, risks, and deal-breakers.
#             - Even minor recurring issues should be reported.

#             Analyze the customer reviews below and return ONLY a valid JSON object
#             that strictly follows this schema (no extra text, no markdown):

#             {schema}

#             Customer Reviews:
#             {reviews}
#         """
#     )

#     model = ChatOpenAI(temperature=0.2)
#     parser = StrOutputParser()

#     chain = prompt | model | parser

#     raw_response = chain.invoke(
#         {
#             "reviews": reviews,
#             "schema": JSON_SCHEMA
#         }
#     )

#     try:
#         return json.loads(raw_response)
#     except json.JSONDecodeError:
#         raise ValueError(f"Invalid JSON returned by LLM:\n{raw_response}")


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

load_dotenv()

JSON_SCHEMA = r"""
{
  "overall_sentiment": "positive | mixed | negative",
  "sentiment_score": 0.0,
  "risk_level": "low | medium | high",
  "deal_breakers": ["string"],
  "most_common_complaints": ["string"],
  "who_should_avoid": "string",
  "summary": "string"
}
"""

def ask_question(
    product_name: str,
    product_price: str,
    product_rating: str,
    reviews: str
) -> dict:
    """
    Receives already-parsed product info and formatted review text.
    DOES NOT parse JSON.stringify input.
    """

    prompt = PromptTemplate.from_template(
        """
            You are an unbiased product review analyst.

            Product Information:
            - Name: {product_name}
            - Price: {product_price}
            - Amazon Rating: {product_rating}

            IMPORTANT:
            - Do NOT assume the product is good just because reviews are mostly positive.
            - Actively look for complaints, risks, and deal-breakers.
            - Even minority recurring issues must be surfaced.

            Analyze the customer reviews below and return ONLY a valid JSON object
            that strictly follows this schema (no extra text, no markdown):

            {schema}

            Customer Reviews:
            {reviews}
        """
    )

    model = ChatOpenAI(temperature=0.2)
    parser = StrOutputParser()

    chain = prompt | model | parser

    raw_response = chain.invoke(
        {
            "product_name": product_name,
            "product_price": product_price,
            "product_rating": product_rating,
            "reviews": reviews,
            "schema": JSON_SCHEMA
        }
    )

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{raw_response}")

