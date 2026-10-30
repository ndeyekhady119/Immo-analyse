
import json
from pathlib import Path

import pandas as pd

from src.processing.load_all import load_all_sources
from src.processing.normalize import normaliser_prix
from src.validation.validate_data import validate_data
from src.processing.export_data import exporter_csv
from src.processing.quality_report import generer_rapport_qualite


def separer_annonces_completes(donnees):
    """
    Sépare les annonces selon la présence
    d'un prix et d'une surface valides.
    Les données originales ne sont pas modifiées.
    """

    prix = donnees["prix"].apply(normaliser_prix)

    surface = pd.to_numeric(
        donnees["surface"]
        .astype(str)
        .str.replace(",", ".", regex=False),
        errors="coerce"
    )

    prix_valide = prix.notna() & (prix > 0)
    surface_valide = surface.notna() & (surface > 0)

    masque_complet = prix_valide & surface_valide

    annonces_completes = donnees.loc[masque_complet].copy()
    annonces_incompletes = donnees.loc[~masque_complet].copy()

    return annonces_completes, annonces_incompletes


def verifier_surfaces_source():
    """
    Compte les surfaces absentes dans le fichier JSON
    des annonces de particuliers.
    """

    chemin = Path("data/raw/particuliers.json")

    if not chemin.exists():
        print("Fichier particuliers.json introuvable.")
        return

    with open(chemin, "r", encoding="utf-8") as fichier:
        donnees_json = json.load(fichier)

    sans_surface = 0

    for element in donnees_json:
        annonce = element.get("annonce", {})
        details = annonce.get("details", {})
        surface = details.get("surface")

        if surface is None or (
            isinstance(surface, str) and surface.strip() == ""
        ):
            sans_surface += 1

    print("\n--- Vérification de la source particuliers ---")
    print("Annonces dans le JSON :", len(donnees_json))
    print("Surfaces absentes dans le JSON :", sans_surface)


def main():
    # 1. Vérifier les données de la source
    verifier_surfaces_source()

    # 2. Charger les cinq sources de données
    donnees = load_all_sources()

    # Conserver une copie des données originales
    donnees_originales = donnees.copy(deep=True)

    print("\n--- Chargement des données ---")
    print("Données chargées :", len(donnees), "annonces")

    # 3. Séparer les annonces complètes et incomplètes
    annonces_completes, annonces_incompletes = (
        separer_annonces_completes(donnees)
    )

    print("\n--- Complétude des annonces ---")
    print("Annonces complètes :", len(annonces_completes))
    print("Annonces incomplètes :", len(annonces_incompletes))

    # 4. Valider les annonces
    conformes, quarantaine = validate_data(donnees)

    print("\n--- Résultats de la validation ---")
    print("Annonces conservées :", len(conformes))
    print("Annonces en quarantaine :", len(quarantaine))

    
    # Vérifier les annonces complètes rejetées par la validation
    ids_completes = set(annonces_completes["id_source"])
    ids_quarantaine = set(quarantaine["id_source"])

    ids_completes_rejetees = ids_completes & ids_quarantaine

    print(
        "\nAnnonces complètes mais rejetées :",
        len(ids_completes_rejetees)
    )

    if ids_completes_rejetees:
        print(
            quarantaine[
                quarantaine["id_source"].isin(ids_completes_rejetees)
            ][
                ["id_source", "prix", "surface", "date", "motif_quarantaine"]
            ].to_string(index=False)
        )


    # 5. Afficher les principaux motifs de quarantaine
    print("\n--- Principaux motifs de quarantaine ---")

    if not quarantaine.empty:
        print(
            quarantaine["motif_quarantaine"]
            .value_counts()
            .head(10)
        )

        print("\nExemples d'annonces en quarantaine :")

        colonnes = [
            colonne
            for colonne in [
                "id_source",
                "date",
                "prix",
                "surface",
                "motif_quarantaine"
            ]
            if colonne in quarantaine.columns
        ]

        print(
            quarantaine[colonnes]
            .head(10)
            .to_string(index=False)
        )
    else:
        print("Aucune annonce en quarantaine.")

    # 6. Exporter les annonces validées et rejetées
    exporter_csv(conformes, "annonces_conformes.csv")
    exporter_csv(quarantaine, "annonces_quarantaine.csv")

    # 7. Générer le rapport de qualité
    generer_rapport_qualite(
    donnees_originales,
    conformes,
    quarantaine,
    annonces_completes,
    annonces_incompletes
    )

    print("\nPipeline terminé !")


if __name__ == "__main__":
    main()
