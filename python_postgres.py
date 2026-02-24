import psycopg2
import random
from datetime import datetime, timedelta, timezone

# ---------------- CONFIG ----------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "metricsdb",
    "user": "appuser",
    "password": "@jB27122020"
}

METRIC_NAME = "myapp_user_request"

START_TIME = datetime(2026, 1, 24, 4, 15, 0, tzinfo=timezone.utc)
END_TIME   = datetime(2026, 2, 8, 12, 24, 0, tzinfo=timezone.utc)

MEAN = 30
STD_DEV = 3
MIN_VALUE = 20
MAX_VALUE = 40

BATCH_SIZE = 1000  # inserts 1000 seconds per batch
# ----------------------------------------


def generate_value():
    v = int(random.gauss(MEAN, STD_DEV))
    return max(MIN_VALUE, min(MAX_VALUE, v))


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    current_time = START_TIME
    rows = []

    print("Starting backfill...")

    while current_time <= END_TIME:
        rows.append((
            current_time,
            METRIC_NAME,
            generate_value()
        ))

        if len(rows) >= BATCH_SIZE:
            cur.executemany(
                """
                INSERT INTO public.metrics (ts, metric_name, value)
                VALUES (%s, %s, %s)
                """,
                rows
            )
            conn.commit()
            print(f"Inserted up to {current_time.isoformat()}")
            rows.clear()

        current_time += timedelta(seconds=1)

    # Insert remaining rows
    if rows:
        cur.executemany(
            """
            INSERT INTO public.metrics (ts, metric_name, value)
            VALUES (%s, %s, %s)
            """,
            rows
        )
        conn.commit()

    cur.close()
    conn.close()

    print("Backfill completed successfully")


if __name__ == "__main__":
    main()

