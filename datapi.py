from fastapi import FastAPI, Depends, HTTPException, status
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Supabase Data API")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

from routes import router 

app.include_router(router)