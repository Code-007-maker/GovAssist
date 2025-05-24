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

# Define 30 schemes
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
    ("Jan Dhan Yojana", "Zero balance bank account.", 18, 99, 500000, "General"),
    
    # Additional schemes
    ("PM Ujjwala Yojana", "Free LPG connections for BPL families.", 18, 99, 200000, "Women"),
    ("Mudra Yojana", "Micro-loans for small businesses.", 18, 60, 800000, "Entrepreneur"),
    ("National Means-cum-Merit Scholarship", "Scholarship for meritorious students.", 12, 18, 300000, "Student"),
    ("Atal Pension Yojana", "Pension scheme for unorganized sector.", 18, 40, 500000, "General"),
    ("Digital India", "Training and support for digital literacy.", 18, 60, 500000, "General"),
    ("PMEGP", "Self-employment through micro enterprises.", 18, 55, 700000, "Entrepreneur"),
    ("Mahila E-Haat", "Online platform for women entrepreneurs.", 18, 99, 1000000, "Women"),
    ("National Social Assistance Program", "Pension for elderly, widows, disabled.", 60, 99, 300000, "General"),
    ("Kanya Sumangala Yojana", "Financial support for girl children.", 0, 18, 400000, "Women"),
    ("Rashtriya Swasthya Bima Yojana", "Health insurance for BPL families.", 0, 99, 300000, "General"),
    ("Saubhagya Yojana", "Free electricity to poor households.", 0, 99, 250000, "General"),
    ("Sukanya Samriddhi Yojana", "Savings scheme for girl child.", 0, 18, 300000, "Women"),
    ("Deen Dayal Upadhyaya Grameen Kaushalya Yojana", "Rural youth employment training.", 18, 35, 450000, "Student"),
    ("Mission Shakti", "Empowerment of women through safety and support.", 18, 60, 500000, "Women"),
    ("Vanbandhu Kalyan Yojana", "Tribal welfare scheme.", 18, 60, 400000, "General"),
    ("Fasal Bima Yojana", "Crop insurance for farmers.", 18, 60, 600000, "Farmer"),
    ("SHG Bank Linkage", "Loans to Self Help Groups.", 18, 60, 500000, "Women"),
    ("National Rural Livelihood Mission", "Self-employment support for rural poor.", 18, 55, 400000, "General"),
    ("National Education Scheme for Disabled", "Educational support for disabled students.", 6, 25, 600000, "Student"),
    ("NIRAMAYA", "Health insurance for persons with disabilities.", 0, 99, 500000, "General"),
    ("Poshan Abhiyaan", "Nutrition for pregnant women and children.", 0, 45, 300000, "Women")
]

# Clear previous data (optional: use with caution)
c.execute("DELETE FROM schemes")

# Insert schemes
c.executemany('''
    INSERT INTO schemes (name, description, min_age, max_age, income_limit, category)
    VALUES (?, ?, ?, ?, ?, ?)
''', schemes)

# Commit and close
conn.commit()
conn.close()

print("Database updated with 30 schemes successfully.")
