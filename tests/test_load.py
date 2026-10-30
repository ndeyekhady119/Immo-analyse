
from src.loaders.load_data import load_json
from src.processing.normalize import normalize_json_data

# Charger le JSON
donnees = load_json("particuliers.json")

# Transformer les données imbriquées en tableau
df = normalize_json_data(donnees)

print("Dimensions du tableau :", df.shape)

print("\nColonnes obtenues :")
print(df.columns.tolist())

print("\nAperçu des cinq premières annonces :")
print(df.head())

print("\nNombre d'identifiants manquants :")
print(df["id_source"].isna().sum())
