import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    dbname="postgres",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    sslmode="require",
    connect_timeout=10,
)

connection.autocommit = True

cursor = connection.cursor()

cursor.execute(
    """
    SELECT 1
    FROM pg_database
    WHERE datname = 'financial_intelligence';
    """
)

if cursor.fetchone():
    print("Database financial_intelligence already exists.")

else:
    cursor.execute(
        "CREATE DATABASE financial_intelligence;"
    )
    print("Database financial_intelligence created successfully.")

cursor.close()
connection.close()