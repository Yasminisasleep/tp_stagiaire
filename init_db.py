import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id TEXT PRIMARY KEY,
        nom TEXT,
        type TEXT,
        solde REAL,
        email TEXT,
        produits_souscrits TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id TEXT PRIMARY KEY,
        nom TEXT,
        type TEXT,
        prix REAL,
        description TEXT,
        tva REAL
    )
""")

clients = [
    ("C001", "Sophie Bernard", "VIP", 28900, "sophie.bernard@email.com", "PROD001,PROD003"),
    ("C002", "Jean Dupont", "Standard", 5200, "jean.dupont@email.com", "PROD002"),
    ("C003", "Marie Curie", "Premium", 15400, "marie.curie@email.com", "PROD001,PROD002,PROD003"),
]

produits = [
    ("PROD001", "Assurance Vie Premium", "Assurance", 150, "Assurance vie avec rendement garanti 3%", 0.0),
    ("PROD002", "PEA Dynamique", "Investissement", 500, "Plan epargne actions avec gestion dynamique", 0.20),
    ("PROD003", "Carte Black Infinite", "Carte bancaire", 300, "Carte premium avec assurances voyage incluses", 0.20),
]

cursor.execute("DELETE FROM clients")
cursor.execute("DELETE FROM produits")

for c in clients:
    cursor.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?)", c)

for p in produits:
    cursor.execute("INSERT INTO produits VALUES (?, ?, ?, ?, ?, ?)", p)

conn.commit()
conn.close()

print("base de donnees initialisee")
