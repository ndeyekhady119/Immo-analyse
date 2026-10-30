
from pathlib import Path

import pandas as pd


# Chemin vers le dossier principal du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Chemin vers le dossier contenant les données brutes
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_csv(file_name, separator=";", encoding="utf-8"):
    """Charge un fichier CSV depuis le dossier data/raw."""
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {file_path}"
        )

    return pd.read_csv(
        file_path,
        sep=separator,
        encoding=encoding
    )

def load_excel(file_name, sheet_name=None):
    """Charge une feuille d'un fichier Excel."""
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    return pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )


def load_json(file_name):
    """Charge un fichier JSON."""
    import json

    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
