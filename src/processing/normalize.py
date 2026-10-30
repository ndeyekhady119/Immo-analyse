
import re
import pandas as pd


def normalize_columns(df, column_mapping):
    """
    Renomme les colonnes d'un DataFrame
    selon un dictionnaire de correspondance.
    """
    df = df.copy()

    df = df.rename(columns=column_mapping)

    # Nettoyer les espaces autour des noms
    df.columns = df.columns.str.strip()

    return df


def normalize_text_values(df):
    """
    Nettoie les valeurs textuelles :
    - supprime les espaces au début et à la fin ;
    - uniformise la casse en minuscules.
    """
    df = df.copy()

    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].map(
            lambda value: (
                value.strip().lower()
                if isinstance(value, str)
                else value
            )
        )

    return df


def normalize_json_data(data):
    """
    Transforme les annonces JSON imbriquées
    en tableau pandas.
    """
    annonces = []

    for element in data:
        annonce = element.get("annonce", {})

        localisation = annonce.get("localisation", {})
        details = annonce.get("details", {})

        ligne = {
            "id_source": annonce.get("id"),
            "date": annonce.get("date"),
            "region": localisation.get("region"),
            "ville": localisation.get("ville"),
            "categorie": details.get("type"),
            "type_transaction": details.get("transaction"),
            "prix": details.get("prix"),
            "surface": details.get("surface"),
            "chambres": details.get("chambres"),
            "salles_bain": details.get("sdb"),
            "statut": annonce.get("statut"),
        }

        annonces.append(ligne)

    return pd.DataFrame(annonces)


def normaliser_prix(valeur):
    """Convertit un prix immobilier en nombre de FCFA."""
    if pd.isna(valeur):
        return None

    if isinstance(valeur, (int, float)):
        return valeur

    texte = str(valeur).strip().lower()

    # Traiter les prix absents ou non chiffrés
    if texte in ["", "à négocier", "a négocier", "non renseigné"]:
        return None

    texte = texte.replace("fcfa", "").strip()
    texte = texte.replace(" ", "")

    # Cas où le prix est exprimé en millions
    if "million" in texte:
        texte = texte.replace("millions", "").replace("million", "")
        try:
            return float(texte.replace(",", ".")) * 1_000_000
        except ValueError:
            return None

    # Conversion d'un prix classique
    texte = texte.replace(",", "")

    try:
        return float(texte)
    except ValueError:
        return None
