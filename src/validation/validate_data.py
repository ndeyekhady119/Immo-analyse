
import pandas as pd
from src.processing.normalize import normaliser_prix


def validate_data(df):
    """
    Sépare les annonces conformes aux règles bloquantes
    des annonces à mettre en quarantaine.
    """

    df = df.copy()

    # Préparer une colonne qui contiendra les motifs
    # de mise en quarantaine.
    df["motif_quarantaine"] = ""

    # 1. Vérifier l'identifiant
    masque_id = (
        df["id_source"].isna()
        | df["id_source"].astype(str).str.strip().eq("")
    )

    df.loc[masque_id, "motif_quarantaine"] += (
        "Identifiant absent; "
    )

    # 2. Vérifier et normaliser le prix
    prix = df["prix"].apply(normaliser_prix)
    df["prix"] = prix

    masque_prix = prix.isna() | (prix <= 0)

    df.loc[masque_prix, "motif_quarantaine"] += (
        "Prix absent ou invalide; "
    )

    # 3. Vérifier et normaliser la surface
    surface = pd.to_numeric(
        df["surface"].astype(str).str.replace(
            ",", ".", regex=False
        ),
        errors="coerce"
    )
    df["surface"] = surface

    masque_surface = surface.isna() | (surface <= 0)

    df.loc[masque_surface, "motif_quarantaine"] += (
        "Surface absente ou invalide; "
    )


    # 3 bis. Signaler les surfaces atypiques
    df["avertissements"] = ""

    masque_surface_atypique = (
        (df["surface"] < 5)
        | (df["surface"] > 2000)
    )

    df.loc[masque_surface_atypique, "avertissements"] += (
        "Surface atypique; "
    )

    # Signaler les prix atypiques
    masque_prix_atypique = (
        (df["prix"] < 100000)
        | (df["prix"] > 2000000000)
    )

    df.loc[masque_prix_atypique, "avertissements"] += (
        "Prix atypique; "
    )

    # 4. Vérifier la date
    date_convertie = pd.to_datetime(
    df["date"],
    errors="coerce",
    format="mixed",
    dayfirst=True
    )

    masque_date = date_convertie.isna()

    df.loc[masque_date, "motif_quarantaine"] += (
        "Date non interprétable; "
    )

    # 5. Vérifier les dates futures pour les annonces vendues
    aujourdhui = pd.Timestamp.today().normalize()

    masque_vendue_future = (
        df["statut"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("vendu")
        & date_convertie.notna()
        & (date_convertie > aujourdhui)
    )

    df.loc[masque_vendue_future, "motif_quarantaine"] += (
        "Date future pour une annonce vendue; "
    )

    # Séparer les annonces
    masque_quarantaine = df["motif_quarantaine"] != ""

    quarantaine = df.loc[masque_quarantaine].copy()

    conformes_aux_regles_bloquantes = df.loc[
        ~masque_quarantaine
    ].copy()

    return conformes_aux_regles_bloquantes, quarantaine
