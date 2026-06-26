import sys, os, json
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

res = sb.table('ai_extracted_products').select(
    'id, name, grade, ingredients_raw, ingredients, verdict, awareness_score'
).ilike('name', 'Parle Monaco Classic').limit(1).execute()

if not res.data:
    print("NOT FOUND")
else:
    row = res.data[0]
    print(f"ID:    {row['id']}")
    print(f"Name:  {row['name']}")
    print(f"Grade: {row['grade']}")
    print(f"Verdict: {row['verdict']}")
    print(f"Awareness: {row['awareness_score']}")
    print(f"\nIngredients raw:\n  {row['ingredients_raw']}")
    print(f"\nClassified ingredients:")
    ings = row.get('ingredients') or []
    if isinstance(ings, str):
        ings = json.loads(ings)
    for i in ings:
        print(f"  [{i['classification']:25s}] {i['name']}")
