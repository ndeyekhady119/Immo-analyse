
# Correspondances pour la plateforme immobilière
PLATEFORME_MAPPING = {
    "ref_plateforme": "id_source",
    "date_mise_en_ligne": "date",
    "type_transaction": "type_transaction",
    "categorie": "categorie",
    "region": "region",
    "commune": "ville",
    "quartier": "quartier",
    "prix": "prix",
    "devise": "devise",
    "surface": "surface",
    "pieces": "pieces",
    "sdb": "salles_bain",
    "statut": "statut",
}

# Correspondances pour les actes notariés
NOTAIRES_MAPPING = {
    "id_acte": "id_source",
    "date_acte": "date",
    "region": "region",
    "ville": "ville",
    "type_bien": "categorie",
    "montant_fcfa": "prix",
    "superficie": "surface",
    "nb_chambres": "chambres",
    "statut": "statut",
}

# Correspondances pour l'historique
HISTORIQUE_MAPPING = {
    "ID": "id_source",
    "DateVente": "date",
    "Region": "region",
    "Ville": "ville",
    "TypeBien": "categorie",
    "Prix": "prix",
    "Surface": "surface",
    "Chambres": "chambres",
    "SallesBain": "salles_bain",
}

# Correspondances pour la feuille Annonces de l'agence
AGENCE_MAPPING = {
    "Code": "id_source",
    "Date": "date",
    "Region": "region",
    "Ville": "ville",
    "Type": "categorie",
    "Prix_FCFA": "prix",
    "Surface_m2": "surface",
    "Chambres": "chambres",
    "SDB": "salles_bain",
    "Statut": "statut",
}
