from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("artigos_db")
DB_USER = os.getenv("postgres")
DB_PASSWORD = os.getenv("23Guigui")
DB_HOST = os.getenv("postgres")
DB_PORT = os.getenv("5433")