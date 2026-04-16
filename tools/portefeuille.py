import yfinance as yf


def calculer_portefeuille(entree):
    lignes = entree.strip().split("|")
    resultats = []
    total = 0
    total_veille = 0

    for ligne in lignes:
        parts = ligne.strip().split(":")
        if len(parts) != 2:
            resultats.append(f"Format invalide : {ligne}")
            continue

        symbole = parts[0].strip().upper()
        try:
            quantite = int(parts[1].strip())
        except ValueError:
            resultats.append(f"Quantite invalide pour {symbole}")
            continue

        try:
            ticker = yf.Ticker(symbole)
            data = ticker.history(period="2d")
            if data.empty:
                resultats.append(f"{symbole} : pas de donnees")
                continue

            cours = data["Close"].iloc[-1]
            valeur = cours * quantite
            total += valeur

            if len(data) >= 2:
                cours_veille = data["Close"].iloc[-2]
                valeur_veille = cours_veille * quantite
                total_veille += valeur_veille
                var = ((cours - cours_veille) / cours_veille) * 100
                resultats.append(f"{symbole} x{quantite} : {cours:.2f}$ -> valeur {valeur:.2f}$ ({var:+.2f}%)")
            else:
                total_veille += valeur
                resultats.append(f"{symbole} x{quantite} : {cours:.2f}$ -> valeur {valeur:.2f}$")
        except Exception as e:
            resultats.append(f"{symbole} : erreur {e}")

    if total_veille > 0:
        variation_globale = ((total - total_veille) / total_veille) * 100
    else:
        variation_globale = 0.0

    resultats.append(f"\nValeur totale du portefeuille : {total:.2f}$")
    resultats.append(f"Variation globale : {variation_globale:+.2f}%")

    return "\n".join(resultats)
