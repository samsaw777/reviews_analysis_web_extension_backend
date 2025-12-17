from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def ask_question(question:str) -> str:
# prompt template
    prompt = PromptTemplate.from_template("{question}")

    model = ChatOpenAI()
    parser = StrOutputParser()

    # chain
    chain = prompt | model | parser

    #result
    result = chain.invoke({"question": question})

    return result