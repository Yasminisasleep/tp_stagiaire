import random


def obtenir_cours_action(symbole):
    cours_simules = {
        "AAPL": 178.50,
        "GOOGL": 141.80,
        "MSFT": 378.90,
        "TSLA": 248.50,
        "AMZN": 182.30,
    }

    symbole = symbole.upper().strip()
    if symbole in cours_simules:
        cours = cours_simules[symbole]
        variation = round(random.uniform(-3, 3), 2)
        return (
            f"Action : {symbole}\n"
            f"Cours actuel : {cours}$\n"
            f"Variation du jour : {variation:+.2f}%"
        )
    return f"Symbole '{symbole}' non trouve."


def calculer_interet(montant, taux, duree):
    try:
        montant = float(montant)
        taux = float(taux)
        duree = int(duree)
        montant_final = montant * (1 + taux / 100) ** duree
        interets = montant_final - montant
        return (
            f"Montant initial : {montant:.2f}e\n"
            f"Taux annuel : {taux}%\n"
            f"Duree : {duree} ans\n"
            f"Montant final : {montant_final:.2f}e\n"
            f"Interets generes : {interets:.2f}e"
        )
    except (ValueError, TypeError) as e:
        return f"Erreur de calcul : {e}"


def convertir_devise(montant, devise_source, devise_cible):
    taux = {
        ("EUR", "USD"): 1.09,
        ("USD", "EUR"): 0.92,
        ("EUR", "GBP"): 0.86,
        ("GBP", "EUR"): 1.16,
        ("USD", "GBP"): 0.79,
        ("GBP", "USD"): 1.27,
    }

    devise_source = devise_source.upper().strip()
    devise_cible = devise_cible.upper().strip()

    if devise_source == devise_cible:
        return f"{float(montant):.2f} {devise_source} = {float(montant):.2f} {devise_cible}"

    paire = (devise_source, devise_cible)
    if paire in taux:
        resultat = float(montant) * taux[paire]
        return (
            f"{float(montant):.2f} {devise_source} = {resultat:.2f} {devise_cible}\n"
            f"Taux de change : 1 {devise_source} = {taux[paire]} {devise_cible}"
        )
    return f"Conversion {devise_source} -> {devise_cible} non disponible."
