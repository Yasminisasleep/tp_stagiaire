CLIENTS = {
    "C001": {
        "nom": "Sophie Bernard",
        "type": "VIP",
        "solde": 28900,
        "email": "sophie.bernard@email.com",
        "produits_souscrits": ["PROD001", "PROD003"]
    },
    "C002": {
        "nom": "Jean Dupont",
        "type": "Standard",
        "solde": 5200,
        "email": "jean.dupont@email.com",
        "produits_souscrits": ["PROD002"]
    },
    "C003": {
        "nom": "Marie Curie",
        "type": "Premium",
        "solde": 15400,
        "email": "marie.curie@email.com",
        "produits_souscrits": ["PROD001", "PROD002", "PROD003"]
    }
}

PRODUITS = {
    "PROD001": {
        "nom": "Assurance Vie Premium",
        "type": "Assurance",
        "prix": 150,
        "description": "Assurance vie avec rendement garanti 3%",
        "tva": 0.0
    },
    "PROD002": {
        "nom": "PEA Dynamique",
        "type": "Investissement",
        "prix": 500,
        "description": "Plan épargne actions avec gestion dynamique",
        "tva": 0.20
    },
    "PROD003": {
        "nom": "Carte Black Infinite",
        "type": "Carte bancaire",
        "prix": 300,
        "description": "Carte premium avec assurances voyage incluses",
        "tva": 0.20
    }
}


def rechercher_client(nom, **kwargs):
    for client_id, client in CLIENTS.items():
        if nom.lower() in client["nom"].lower():
            produits = ", ".join(client["produits_souscrits"])
            return (
                f"Client trouvé : {client['nom']} (ID: {client_id})\n"
                f"Type : {client['type']}\n"
                f"Solde : {client['solde']}€\n"
                f"Email : {client['email']}\n"
                f"Produits souscrits : {produits}"
            )
    return f"Aucun client trouvé avec le nom '{nom}'"


def rechercher_produit(nom, **kwargs):
    for produit_id, produit in PRODUITS.items():
        if nom.lower() in produit["nom"].lower():
            return (
                f"Produit trouvé : {produit['nom']} (ID: {produit_id})\n"
                f"Type : {produit['type']}\n"
                f"Prix : {produit['prix']}€\n"
                f"Description : {produit['description']}\n"
                f"TVA : {int(produit['tva'] * 100)}%"
            )
    return f"Aucun produit trouvé avec le nom '{nom}'"
