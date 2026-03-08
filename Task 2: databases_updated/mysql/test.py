from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DB = os.getenv("MYSQL_DB")

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

try:
    with engine.connect() as conn:
        # Wrap the SQL string in text()
        result = conn.execute(text("SHOW DATABASES;"))
        print("Databases on this server:")
        for row in result:
            print(row[0])
except Exception as e:
    print("Error connecting to MySQL:")
    print(e)