"""
Fix SQL file to convert string aliases to proper PostgreSQL array format
Run this script to fix the ingredients_500_extended.sql file
"""

import re

# Read the SQL file
with open('database/ingredients_500_extended.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Function to convert string aliases to array format
def convert_aliases(match):
    full_match = match.group(0)
    aliases_str = match.group(1)
    
    # If it's already an ARRAY format, skip it
    if aliases_str.startswith('ARRAY['):
        return full_match
    
    # Remove the quotes around the aliases string
    aliases_str = aliases_str.strip("'")
    
    # Split by comma and create array elements
    if aliases_str:
        aliases_list = [f"'{alias.strip()}'" for alias in aliases_str.split(',')]
        array_str = f"ARRAY[{', '.join(aliases_list)}]"
    else:
        array_str = "ARRAY[]::text[]"
    
    # Replace in the original match
    result = full_match.replace(f"'{match.group(1)}'", array_str)
    return result

# Pattern to match: ('Name', 'aliases string', 'classification', ...)
# We need to match the second field (aliases) and convert it
pattern = r"\('([^']+)',\s*'([^']*)',\s*'(generally_recognised|worth_knowing|commonly_questioned)'"

def fix_line(match):
    name = match.group(1)
    aliases = match.group(2)
    classification = match.group(3)
    
    # Convert aliases to array format
    if aliases:
        aliases_list = [f"'{alias.strip()}'" for alias in aliases.split(',')]
        array_str = f"ARRAY[{', '.join(aliases_list)}]"
    else:
        array_str = "ARRAY[]::text[]"
    
    return f"('{name}', {array_str}, '{classification}'"

# Apply the fix
content = re.sub(pattern, fix_line, content)

# Write back
with open('database/ingredients_500_extended.sql', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all aliases to proper array format!")
print("Now run the SQL file in Supabase")
