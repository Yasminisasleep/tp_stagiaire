import yfinance as yf


def obtenir_cours_action(symbole):
    symbole = symbole.upper().strip()
    try:
        ticker = yf.Ticker(symbole)
        data = ticker.history(period="2d")
        if data.empty:
            return f"Symbole '{symbole}' non trouve ou pas de donnees."

        cours_actuel = data["Close"].iloc[-1]
        if len(data) >= 2:
            cours_veille = data["Close"].iloc[-2]
            variation = ((cours_actuel - cours_veille) / cours_veille) * 100
        else:
            variation = 0.0
        volume = data["Volume"].iloc[-1]

        return (
            f"Action : {symbole}\n"
            f"Cours actuel : {cours_actuel:.2f}$\n"
            f"Variation du jour : {variation:+.2f}%\n"
            f"Volume : {int(volume)}"
        )
    except Exception as e:
        return f"Erreur lors de la recuperation du cours de {symbole} : {e}"


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
