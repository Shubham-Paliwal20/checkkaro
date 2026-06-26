import sys, os, json
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])

ids = [
    '3dcee136-9f58-49ab-81a6-d624cb2129ea',
    '77421d1d-99ae-4697-a139-590498fc4439',
    'b24b5aa8-a479-427a-8a62-9b03d8fe2a70',
]
for rid in ids:
    res = sb.table('ai_extracted_products').select(
        'id, name, grade, ingredients_raw, ingredients'
    ).eq('id', rid).execute()
    row = res.data[0]
    print(f"\n=== {row['name']} ({row['id'][:8]}) Grade={row['grade']} ===")
    print(f"  raw: {row['ingredients_raw']}")
    ings = row.get('ingredients') or []
    if isinstance(ings, str):
        ings = json.loads(ings)
    for i in (ings if isinstance(ings, list) else []):
        if isinstance(i, dict):
            print(f"  [{i.get('classification','?'):25s}] {i.get('name','?')}")
        else:
            print(f"  {i}")
