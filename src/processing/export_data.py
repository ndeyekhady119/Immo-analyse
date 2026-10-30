
from pathlib import Path


def exporter_csv(df, nom_fichier):
    """
    Enregistre un DataFrame dans un fichier CSV.
    """

    dossier_sortie = Path("data/processed")
    dossier_sortie.mkdir(parents=True, exist_ok=True)

    chemin_fichier = dossier_sortie / nom_fichier

    df.to_csv(
        chemin_fichier,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Fichier exporté : {chemin_fichier}")
