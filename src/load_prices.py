import os
import psycopg2
from psycopg2.extras import execute_values

from fetch_prices import fetch_prices, SYMBOLS

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS prices (
    symbol    TEXT NOT NULL,
    date      DATE NOT NULL,
    open      NUMERIC(18, 6),
    high      NUMERIC(18, 6),
    low       NUMERIC(18, 6),
    close     NUMERIC(18, 6),
    volume    BIGINT,
    loaded_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (symbol, date)
);
"""

UPSERT = """
INSERT INTO prices (symbol, date, open, high, low, close, volume)
VALUES %s
ON CONFLICT (symbol, date) DO UPDATE SET
    open = EXCLUDED.open,
    high = EXCLUDED.high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    volume = EXCLUDED.volume,
    loaded_at = now();
"""

def load_prices():
    data = fetch_prices(SYMBOLS)
    rows = [tuple(r) for r in data.astype(object).itertuples(index=False)]

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        with conn, conn.cursor() as cur:
            cur.execute(CREATE_TABLE)
            execute_values(cur, UPSERT, rows)
    finally:
        conn.close()
    print(f"Loaded {len(rows)} rows into prices")

if __name__ == "__main__":
    load_prices()