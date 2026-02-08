from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

prompt = PromptTemplate.from_template(
    open("prompt.txt").read()
)

def question_to_sql(question: str) -> str:
    prompt_text = prompt.format(question=question)
    response = llm.invoke(prompt_text)
    return response.content.strip()

