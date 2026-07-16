import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SECRET_KEY=os.getenv("SECRET_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Add this temporary debugging code to db.py:
print("--- .env verification ---")
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", "FOUND" if os.getenv("SUPABASE_KEY") else "MISSING")
print("SECRET_KEY:", "FOUND" if os.getenv("SECRET_KEY") else "MISSING")
print("------------------------------")