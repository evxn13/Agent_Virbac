# Mini agent : question sur une entreprise francaise,
# cherche lui meme les infos sur l'API officielle (base SIRENE de l'INSEE).
# Idee venue d'Eligence.ai : la on donnait tout au modele en entree, ici c'est lui qui decide quand aller chercher les donnees.
# Lancer : export GEMINI_API_KEY="..." puis python3 agent.py

import json
import os
import urllib.error
import urllib.parse
import urllib.request

# la cle reste dans l'env, jamais dans le code
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

# quota gratuit = par modele, donc si l'un est a sec (429) ou sature (503) on passe au suivant
# dict.fromkeys = enleve les doublons en gardant l'ordre
MODELES = list(dict.fromkeys([MODEL, "gemini-flash-lite-latest", "gemini-3.5-flash", "gemini-flash-latest"]))

SYSTEM_PROMPT = (
    "Tu es un assistant qui renseigne sur les entreprises françaises. "
    "Utilise toujours l'outil rechercher_entreprise pour obtenir des données officielles, "
    "n'invente jamais une information. Si plusieurs entreprises sont concernées, "
    "appelle l'outil plusieurs fois. Réponds en français, de façon concise."
)


# --- l'outil ---

def rechercher_entreprise(recherche: str) -> dict:
    """Cherche une entreprise via l'API Recherche d'entreprises (gratuite, sans cle)."""
    params = urllib.parse.urlencode({"q": recherche, "per_page": 3})
    url = f"https://recherche-entreprises.api.gouv.fr/search?{params}"
    with urllib.request.urlopen(url, timeout=10) as reponse:
        data = json.load(reponse)

    # l'API renvoie enormement de champs, je garde que l'utile
    # -> moins de tokens et le modele se perd moins
    resultats = []
    for e in data.get("results", []):
        siege = e.get("siege") or {}
        resultats.append({
            "nom": e.get("nom_complet"),
            "siren": e.get("siren"),
            "siret_siege": siege.get("siret"),
            "adresse_siege": siege.get("adresse"),
            "date_creation": e.get("date_creation"),
            "code_naf": e.get("activite_principale"),
            "categorie": e.get("categorie_entreprise"),  # PME / ETI / GE
            "tranche_effectif_code": e.get("tranche_effectif_salarie"),
            "etat": "active" if e.get("etat_administratif") == "A" else "fermée",
            "nb_etablissements_ouverts": e.get("nombre_etablissements_ouverts"),
        })
    return {"resultats": resultats}


# ce que le modele voit de l'outil (il voit jamais le code, a part :)
TOOLS = [{
    "functionDeclarations": [{
        "name": "rechercher_entreprise",
        "description": "Recherche une entreprise française par nom, SIREN ou SIRET "
                       "dans la base officielle SIRENE de l'INSEE.",
        "parameters": {
            "type": "object",
            "properties": {
                "recherche": {
                    "type": "string",
                    "description": "Nom de l'entreprise, numéro SIREN (9 chiffres) ou SIRET (14 chiffres)",
                }
            },
            "required": ["recherche"],
        },
    }]
}]

# nom de l'outil -> vraie fonction (pour en rajouter un, une ligne ici + sa description au-dessus)
FONCTIONS = {"rechercher_entreprise": rechercher_entreprise}


# --- appel a Gemini, en HTTP direct sans SDK ---

def appeler_gemini(historique: list) -> dict:
    corps = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": historique,
        "tools": TOOLS,
    }
    data = json.dumps(corps).encode()

    for modele in MODELES:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent"
        requete = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY},
        )
        try:
            with urllib.request.urlopen(requete, timeout=60) as reponse:
                return json.load(reponse)
        except urllib.error.HTTPError as erreur:
            # 429 = quota depasse, 503 = surcharge, 404 = modele retire -> on tente le suivant
            if erreur.code in (404, 429, 503):
                print(f"  [gemini] {modele} indisponible ({erreur.code}), modele suivant...")
            else:
                raise  # autre erreur (cle invalide...) : on la laisse remonter

    raise RuntimeError("Tous les modeles sont indisponibles (quota ou surcharge), reessaie plus tard.")


# --- la boucle d'agent ---
# question -> le modele demande un outil -> j'execute -> je lui renvoie le resultat
# -> jusqu'a ce qu'il reponde en texte

def agent(question: str, max_etapes: int = 5) -> str:
    historique = [{"role": "user", "parts": [{"text": question}]}]

    for _ in range(max_etapes):  # au cas ou il boucle, securité cout
        reponse = appeler_gemini(historique)
        contenu = reponse["candidates"][0]["content"]
        historique.append(contenu)  # pas de memoire = renvoyer

        appels = [p["functionCall"] for p in contenu["parts"] if "functionCall" in p]
        if not appels:
            # plus d'outil demande = il a fini
            return "".join(p.get("text", "") for p in contenu["parts"])

        resultats = []
        for appel in appels:
            print(f"  [outil] {appel['name']}({appel.get('args', {})})")
            try:
                resultat = FONCTIONS[appel["name"]](**appel.get("args", {}))
            except Exception as erreur:
                # API HANDLE
                resultat = {"erreur": str(erreur)}
            resultats.append({"functionResponse": {"name": appel["name"], "response": resultat}})

        historique.append({"role": "user", "parts": resultats})

    return "Nombre maximum d'étapes atteint."


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        raise SystemExit("Définis d'abord la variable GEMINI_API_KEY.")
    print("Mini agent entreprises (Ctrl+C pour quitter)")
    while True:
        question = input("\nQuestion > ").strip()
        if question:
            try:
                print("\n" + agent(question))
            except Exception as erreur:
                # pas de crash en pleine demo : on affiche l'erreur et on continue 
                print(f"\n[erreur] {erreur}")
# 01:22AM
