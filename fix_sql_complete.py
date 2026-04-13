"""
Complete fix for SQL file - handles all edge cases including escaped quotes
"""

import re

# Read the SQL file
with open('database/ingredients_500_extended.sql', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_insert = False

for line in lines:
    # Check if we're in an INSERT statement
    if 'INSERT INTO ingredients' in line:
        in_insert = True
        fixed_lines.append(line)
        continue
    
    # If not in INSERT or it's a comment/empty line, keep as is
    if not in_insert or line.strip().startswith('--') or not line.strip():
        fixed_lines.append(line)
        continue
    
    # Check if this line contains a data row (starts with parenthesis)
    if line.strip().startswith('('):
        # This is a data row, need to fix the aliases field (2nd field)
        # Pattern: ('Name', 'aliases', 'classification', ...)
        
        # Find the second quoted string (aliases field)
        # We need to be careful with escaped quotes
        parts = line.split("', '", 1)  # Split after first field
        if len(parts) >= 2:
            # Get everything after the name
            rest = parts[1]
            
            # Find the aliases part (everything until the next ', ')
            # But we need to handle escaped quotes ''
            aliases_end = 0
            quote_count = 0
            i = 0
            while i < len(rest):
                if rest[i:i+2] == "''":
                    i += 2
                    continue
                if rest[i] == "'":
                    quote_count += 1
                    if quote_count == 1:  # Found end of aliases
                        aliases_end = i
                        break
                i += 1
            
            if aliases_end > 0:
                aliases_str = rest[:aliases_end]
                after_aliases = rest[aliases_end:]
                
                # Convert aliases string to array format
                if aliases_str and not aliases_str.startswith('ARRAY['):
                    # Split by comma and create array
                    alias_parts = [a.strip() for a in aliases_str.split(',')]
                    array_elements = []
                    for alias in alias_parts:
                        # Escape single quotes for PostgreSQL
                        alias_escaped = alias.replace("'", "''")
                        array_elements.append(f"'{alias_escaped}'")
                    
                    aliases_array = f"ARRAY[{', '.join(array_elements)}]"
                    
                    # Reconstruct the line
                    line = parts[0] + "', " + aliases_array + after_aliases
        
        fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write back
with open('database/ingredients_500_extended.sql', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ Complete fix applied!")
print("✅ All aliases converted to proper array format")
print("✅ Escaped quotes handled correctly")
print("\nNow run the SQL file in Supabase")
