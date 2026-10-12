import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('renderAdminPanel')
print(c[idx:idx+3500])

idx2 = c.find('renderAdminSubtabContent')
print("\n--- SUBTAB CONTENT ---")
print(c[idx2:idx2+2500])
