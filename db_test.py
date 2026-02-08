import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="metricsdb",
    user="llm_user",
    password="llm_pass"
)

cur = conn.cursor()
cur.execute("SELECT NOW();")
print(cur.fetchone())

conn.close()

