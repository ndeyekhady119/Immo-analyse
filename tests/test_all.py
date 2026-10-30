
from src.processing.load_all import load_all_sources

# Charger et fusionner les cinq sources
donnees = load_all_sources()

print("Dimensions du tableau fusionné :", donnees.shape)

print("\nNombre d'annonces par source :")
print(donnees["source"].value_counts())

print("\nColonnes disponibles :")
print(donnees.columns.tolist())

print("\nAperçu des cinq premières annonces :")
print(donnees.head())


print("\nNombre de valeurs manquantes par colonne :")
print(donnees.isna().sum().sort_values(ascending=False))

print("\nPourcentage de valeurs manquantes par colonne :")
print(
    (donnees.isna().mean() * 100)
    .round(2)
    .sort_values(ascending=False)
)


print("\nValeurs manquantes par source :")

manquants_source = donnees.groupby("source").apply(
    lambda groupe: groupe.isna().sum()
)

print(manquants_source.T)


print("\nExemples de prix par source :")

for nom_source, groupe in donnees.groupby("source"):
    print(f"\n--- {nom_source} ---")
    print(groupe["prix"].dropna().head(10).tolist())
