import psycopg2

def run_sql(sql: str):
    if not sql.lower().startswith("select"):
        raise Exception("Only SELECT queries allowed")

    forbidden = ["delete", "update", "insert", "drop", "alter"]
    if any(word in sql.lower() for word in forbidden):
        raise Exception("Unsafe SQL detected")

    conn = psycopg2.connect(
        host="localhost",
        dbname="metricsdb",
        user="llm_user",
        password="llm_pass"
    )

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    conn.close()
    return rows

