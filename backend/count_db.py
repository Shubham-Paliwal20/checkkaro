import re

text = open('routes/ingredient_database.py', encoding='utf-8').read()

desc_count = len(__import__('routes.ingredient_database', fromlist=['INGREDIENT_DESCRIPTIONS']).INGREDIENT_DESCRIPTIONS)

def count_keys(block):
    return len(re.findall(r"^\s+'[^']+'\s*:\s*\(", block, re.MULTILINE))

cq = re.search(r'commonly_questioned_patterns\s*=\s*\{(.+?)worth_knowing_patterns', text, re.DOTALL)
wk = re.search(r'worth_knowing_patterns\s*=\s*\{(.+?)generally_recognised_patterns', text, re.DOTALL)
gr = re.search(r'generally_recognised_patterns\s*=\s*\{(.+?)\}\s*\n\s*#\s*For cosmetic', text, re.DOTALL)

cq_n = count_keys(cq.group(1)) if cq else 0
wk_n = count_keys(wk.group(1)) if wk else 0
gr_n = count_keys(gr.group(1)) if gr else 0

print(f"INGREDIENT_DESCRIPTIONS (factual descriptions) : {desc_count}")
print(f"commonly_questioned patterns (RED)             : {cq_n}")
print(f"worth_knowing patterns (YELLOW)                : {wk_n}")
print(f"generally_recognised patterns (GREEN)          : {gr_n}")
print(f"Total classification patterns                  : {cq_n + wk_n + gr_n}")
print(f"Grand total across all sections                : {desc_count + cq_n + wk_n + gr_n}")
