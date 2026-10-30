
from src.loaders.load_data import load_csv, load_excel, load_json
from src.processing.normalize import normalize_columns, normalize_json_data
from src.processing.mappings import (
    PLATEFORME_MAPPING,
    NOTAIRES_MAPPING,
    HISTORIQUE_MAPPING,
    AGENCE_MAPPING,
)


def load_all_sources():
    """Charge les cinq sources immobilières."""

    # 1. Plateforme immobilière
    plateforme = load_csv(
        "plateforme_immo_sn.csv",
        separator=";"
    )
    plateforme = normalize_columns(
        plateforme, PLATEFORME_MAPPING
    )
    plateforme["source"] = "plateforme"

    # 2. Actes notariés
    notaires = load_csv(
        "notaires.csv",
        separator=","
    )
    notaires = normalize_columns(
        notaires, NOTAIRES_MAPPING
    )
    notaires["source"] = "notaires"

    # 3. Historique
    historique = load_csv(
        "import_historique.csv",
        separator=";",
        encoding="latin-1"
    )
    historique = normalize_columns(
        historique, HISTORIQUE_MAPPING
    )
    historique["source"] = "historique"

    # 4. Agence immobilière : feuille Annonces
    agence = load_excel(
        "agence_teranga.xlsx",
        sheet_name="Annonces"
    )
    agence = normalize_columns(
        agence, AGENCE_MAPPING
    )
    agence["source"] = "agence"

    # 5. Particuliers : fichier JSON
    donnees_json = load_json("particuliers.json")
    particuliers = normalize_json_data(donnees_json)
    particuliers["source"] = "particuliers"

    # Fusionner les sources sans supprimer de données
    donnees = __import__("pandas").concat(
        [
            plateforme,
            notaires,
            historique,
            agence,
            particuliers,
        ],
        ignore_index=True,
        sort=False
    )

    return donnees
