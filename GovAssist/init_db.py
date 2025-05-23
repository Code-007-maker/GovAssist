import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('schemes.db')
c = conn.cursor()

# Create the schemes table
c.execute('''
CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    min_age INTEGER,
    max_age INTEGER,
    income_limit INTEGER,
    category TEXT
)
''')

# Insert 10 sample schemes
schemes = [
    ("PM Kisan", "Income support for farmers.", 18, 60, 150000, "Farmer"),
    ("Ayushman Bharat", "Health insurance for low-income families.", 0, 99, 300000, "General"),
    ("Startup India", "Support for startups.", 18, 40, 1200000, "Entrepreneur"),
    ("UDAN Scheme", "Airfare subsidy for underserved regions.", 18, 99, 500000, "General"),
    ("Beti Bachao Beti Padhao", "Support for girl child education.", 0, 18, 400000, "Women"),
    ("National Apprenticeship Promotion", "Stipends for apprentices.", 16, 30, 600000, "Student"),
    ("Stand-Up India", "Loans for women and SC/ST entrepreneurs.", 21, 60, 800000, "Women"),
    ("Pradhan Mantri Awas Yojana", "Affordable housing.", 18, 60, 600000, "General"),
    ("Skill India", "Free skill training.", 18, 45, 400000, "Student"),
    ("Jan Dhan Yojana", "Zero balance bank account.", 18, 99, 500000, "General")
]

# Insert into table
c.executemany('''
    INSERT INTO schemes (name, description, min_age, max_age, income_limit, category)
    VALUES (?, ?, ?, ?, ?, ?)
''', schemes)

# Save and close
conn.commit()
conn.close()

print("Database and sample schemes created successfully.")
