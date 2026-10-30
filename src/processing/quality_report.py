
from pathlib import Path
import json


def generer_rapport_qualite(
    donnees_initiales,
    conformes,
    quarantaine,
    annonces_completes=None,
    annonces_incompletes=None
):
    total = len(donnees_initiales)
    nb_conformes = len(conformes)
    nb_quarantaine = len(quarantaine)

    nb_completes = (
        len(annonces_completes)
        if annonces_completes is not None
        else None
    )

    nb_incompletes = (
        len(annonces_incompletes)
        if annonces_incompletes is not None
        else None
    )

    nb_avec_avertissements = 0

    if "avertissements" in conformes.columns:
        nb_avec_avertissements = int(
            conformes["avertissements"]
            .fillna("")
            .str.strip()
            .ne("")
            .sum()
        )

    taux_conservation = (
        round(nb_conformes / total * 100, 2)
        if total > 0 else 0
    )

    taux_quarantaine = (
        round(nb_quarantaine / total * 100, 2)
        if total > 0 else 0
    )

    rapport = {
        "nombre_total": total,
        "annonces_conformes": nb_conformes,
        "annonces_quarantaine": nb_quarantaine,
        "annonces_avec_avertissements": nb_avec_avertissements,
        "taux_conservation": taux_conservation,
        "taux_quarantaine": taux_quarantaine
    }

    if nb_completes is not None:
        rapport["annonces_completes"] = nb_completes
        rapport["taux_completude"] = (
            round(nb_completes / total * 100, 2)
            if total > 0 else 0
        )

    if nb_incompletes is not None:
        rapport["annonces_incompletes"] = nb_incompletes

    dossier_sortie = Path("data/processed")
    dossier_sortie.mkdir(parents=True, exist_ok=True)

    chemin_fichier = dossier_sortie / "rapport_qualite.json"

    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(rapport, fichier, ensure_ascii=False, indent=4)

    print(f"Rapport de qualité exporté : {chemin_fichier}")
