import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Validate environment variables
if not SUPABASE_URL:
    raise ValueError(
        "SUPABASE_URL environment variable is not set. "
        "Please add it to your .env file."
    )

if not SUPABASE_ANON_KEY:
    raise ValueError(
        "SUPABASE_ANON_KEY environment variable is not set. "
        "Please add it to your .env file."
    )

# Create and export Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
