from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Auth Functions
def register_user(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

def login_user(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def get_user(session_token):
    user = supabase.auth.get_user(session_token)
    return user
