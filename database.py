import sqlite3

DB_PATH = "database.db"


def rechercher_client(nom, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, type, solde, email, produits_souscrits FROM clients WHERE LOWER(nom) LIKE ?", (f"%{nom.lower()}%",))
    row = cursor.fetchone()
    conn.close()

    if row:
        return (
            f"Client trouve : {row[1]} (ID: {row[0]})\n"
            f"Type : {row[2]}\n"
            f"Solde : {row[3]}e\n"
            f"Email : {row[4]}\n"
            f"Produits souscrits : {row[5]}"
        )
    return f"Aucun client trouve avec le nom '{nom}'"


def rechercher_produit(nom, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, type, prix, description, tva FROM produits WHERE LOWER(nom) LIKE ?", (f"%{nom.lower()}%",))
    row = cursor.fetchone()
    conn.close()

    if row:
        return (
            f"Produit trouve : {row[1]} (ID: {row[0]})\n"
            f"Type : {row[2]}\n"
            f"Prix : {row[3]}e\n"
            f"Description : {row[4]}\n"
            f"TVA : {int(row[5] * 100)}%"
        )
    return f"Aucun produit trouve avec le nom '{nom}'"
