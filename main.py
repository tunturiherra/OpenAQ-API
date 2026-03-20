import psycopg2
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI()

# yhteys tietokantaan tällä
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PWD"),
    )