
import pandas as pd
from src.validation.validate_data import validate_data
from src.processing.normalize import normaliser_prix
from src.processing.export_data import exporter_csv
from src.processing.quality_report import generer_rapport_qualite

# Créer trois annonces de test

donnees_test = pd.DataFrame([
    {
        "id_source": "TEST001",
        "prix": 50000000,
        "surface": 100,
        "date": "15/03/2024",
        "statut": "En vente",
    },
    {
        "id_source": "TEST002",
        "prix": 0,
        "surface": 80,
        "date": "10/06/2023",
        "statut": "Vendu",
    },
    {
        "id_source": "TEST003",
        "prix": 30000000,
        "surface": 0,
        "date": "32/13/2024",
        "statut": "En vente",
    },
    {
        "id_source": "TEST004",
        "prix": 45000000,
        "surface": 90,
        "date": "31/12/2099",
        "statut": "Vendu",
    },
    {
    "id_source": "TEST005",
    "prix": 50000,
    "surface": 3,
    "date": "15/03/2024",
    "statut": "En vente"
    },
])

conformes, quarantaine = validate_data(donnees_test)

print("\nAvertissements des annonces conservées :")
print(
    conformes[
        ["id_source", "prix", "surface", "avertissements"]
    ]
)

print("Annonces conservées :", len(conformes))
print("Annonces en quarantaine :", len(quarantaine))

print("\nMotifs de quarantaine :")
print(quarantaine[["id_source", "motif_quarantaine"]])

print("\nTest de normalisation des prix :")
 
prix_a_tester = [
    "26 620 000",
    "65575000 FCFA",
    "57.62 millions",
    490000,
]

for prix in prix_a_tester:
    print(prix, "->", normaliser_prix(prix))

print("\nTest de normalisation des surfaces :")

surfaces_a_tester = [
    "75,5",
    "120",
    85.0,
    "abc",
]

for surface in surfaces_a_tester:
    print(surface, "->", pd.to_numeric(
        str(surface).replace(",", "."),
        errors="coerce"
    ))  

print("\nTest de validation des dates :")

dates_a_tester = [
    "15/03/2024",
    "2024-03-15",
    "32/13/2024",
    "date_invalide",
]

for date in dates_a_tester:
    if "-" in date and len(date) == 10:
        resultat = pd.to_datetime(
        date,
        format="%Y-%m-%d",
        errors="coerce"
    )
    else:
        resultat = pd.to_datetime(
        date,
        format="%d/%m/%Y",
        errors="coerce"
    )
    print(date, "->", resultat)

total = len(donnees_test)
nb_conformes = len(conformes)
nb_quarantaine = len(quarantaine)
nb_avec_avertissements = (
    conformes["avertissements"].str.strip().ne("").sum()
)

print("\n--- Indicateurs de qualité ---")
print("Nombre total d'annonces :", total)
print("Annonces conservées :", nb_conformes)
print("Annonces en quarantaine :", nb_quarantaine)
print("Annonces avec avertissements :", nb_avec_avertissements)
print(
    "Taux de conservation :",
    round(nb_conformes / total * 100, 2),
    "%"
)

# Test d'export des annonces conformes
exporter_csv(conformes, "annonces_conformes.csv")

# Test d'export des annonces en quarantaine
exporter_csv(quarantaine, "annonces_quarantaine.csv")

# Générer le rapport de qualité
generer_rapport_qualite(
    donnees_test,
    conformes,
    quarantaine
)