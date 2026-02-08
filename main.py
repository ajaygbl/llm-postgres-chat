from fastapi import FastAPI
from sql_generator import question_to_sql
from db import run_sql

app = FastAPI()

@app.get("/ask")
def ask(question: str):
    sql = question_to_sql(question)
    result = run_sql(sql)

    return {
        "question": question,
        "sql": sql,
        "result": result
    }

