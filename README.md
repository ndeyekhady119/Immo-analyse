# ImmoAnalyse — Nettoyage et contrôle qualité des données immobilières

## 1. Présentation du projet

**ImmoAnalyse** est un projet de traitement et de contrôle qualité de données immobilières. Il a pour objectif de centraliser plusieurs sources de données immobilières, de les harmoniser, de détecter les incohérences et de produire un jeu de données fiable pouvant être utilisé pour des analyses statistiques et de visualisation.

Les données proviennent de différentes sources : plateformes immobilières, agences, particuliers, historiques d'importation et données notariales.

Ces sources peuvent présenter des différences de format, des informations manquantes, des doublons ou des valeurs incorrectes. Le projet met donc en place un processus automatisé de nettoyage, de normalisation et de validation.

## 2. Objectifs du projet

Les principaux objectifs sont les suivants :

- Collecter et fusionner les données provenant de plusieurs fichiers.
- Harmoniser les formats et les types de données.
- Normaliser les informations telles que les prix, les surfaces et les dates.
- Vérifier la cohérence des données à l'aide de règles métier.
- Identifier les annonces conformes et celles qui présentent des anomalies.
- Séparer les données exploitables des données à corriger.
- Générer un rapport de qualité permettant de mesurer la fiabilité du jeu de données.
- Réaliser une analyse exploratoire afin de mieux comprendre les données immobilières.

## 3. Sources de données

Le projet exploite cinq fichiers sources, regroupés dans le dossier `data/raw/`.

| Fichier | Source |
|---|---|
| `plateforme_immo_sn.csv` | Plateforme immobilière |
| `agence_teranga.xlsx` | Agence immobilière Teranga |
| `particuliers.json` | Annonces de particuliers |
| `import_historique.csv` | Historique des importations |
| `notaires.csv` | Données notariales |

Les données sont hétérogènes : elles ne présentent pas nécessairement les mêmes noms de colonnes, les mêmes formats ou le même niveau de complétude.

Le traitement consiste donc à les rendre compatibles avant leur analyse.

## 4. Architecture du projet

Le projet est organisé de manière à séparer les données, les traitements, les validations et les analyses.

```text
immo-analyse/
│
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── agence_teranga.xlsx
│   │   ├── import_historique.csv
│   │   ├── notaires.csv
│   │   ├── particuliers.json
│   │   └── plateforme_immo_sn.csv
│   │
│   ├── references/
│   │   ├── dictionnaire_donnees.csv
│   │   ├── referentiel_categories.csv
│   │   ├── referentiel_geographique.csv
│   │   └── regles_metier.md
│   │
│   └── processed/
│       ├── annonces_conformes.csv
│       ├── annonces_quarantaine.csv
│       └── rapport_qualite.json
│
├── notebooks/
│   └── eda_analyse_exploratoire.ipynb
│
└── src/
    ├── loaders/
    │   └── load_data.py
    │
    ├── processing/
    │   ├── export_data.py
    │   ├── load_all.py
    │   ├── mappings.py
    │   ├── normalize.py
    │   └── quality_report.py
    │
    └── validation/
        └── validate_data.py
```

### Rôle des principaux dossiers

**`data/raw/`**

Contient les fichiers originaux importés depuis les différentes sources. Ces fichiers sont conservés afin de préserver les données avant transformation.

**`data/references/`**

Contient les fichiers de référence utilisés pour guider le traitement : dictionnaire des données, référentiel des catégories, référentiel géographique et règles métier.

**`data/processed/`**

Contient les fichiers générés à la fin du traitement : annonces conformes, annonces mises en quarantaine et rapport de qualité.

**`src/loaders/`**

Contient les fonctions permettant de lire les différents formats de fichiers et de charger les données.

**`src/processing/`**

Regroupe les opérations de fusion, de normalisation, de préparation, d'exportation et de génération du rapport de qualité.

**`src/validation/`**

Contient les règles de contrôle permettant de vérifier la conformité des annonces.

**`notebooks/`**

Contient le notebook consacré à l'analyse exploratoire des données (EDA).

## 5. Technologies et bibliothèques utilisées

Le projet est développé principalement avec Python.

| Outil ou bibliothèque | Utilisation |
|---|---|
| Python | Langage principal |
| Pandas | Manipulation, fusion et analyse des données |
| NumPy | Opérations numériques |
| OpenPyXL | Lecture des fichiers Excel |
| JSON | Lecture et génération de données au format JSON |
| Jupyter Notebook | Analyse exploratoire |
| VS Code | Environnement de développement |

## 6. Installation et configuration

### Prérequis

Avant de commencer, il est nécessaire de disposer de :

- Python installé sur la machine.
- Visual Studio Code ou un autre éditeur de code.
- Git (facultatif, pour la gestion du projet).

### Étape 1 : ouvrir le dossier du projet

Ouvrir le dossier `immo-analyse` dans VS Code.

### Étape 2 : créer un environnement virtuel

Dans le terminal de VS Code, exécuter :

```bash
python -m venv .venv
```

### Étape 3 : activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Windows CMD :

```cmd
.venv\Scripts\activate.bat
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

### Étape 4 : installer les dépendances

```bash
pip install -r requirements.txt
```

## 7. Exécution du pipeline

Le traitement principal est lancé depuis le fichier `main.py`.

Dans le terminal, à la racine du projet, exécuter :

```bash
python main.py
```

Le programme réalise les principales étapes suivantes :

1. Chargement des fichiers provenant des différentes sources.
2. Regroupement des données dans une structure commune.
3. Normalisation des informations.
4. Vérification des règles de qualité.
5. Séparation des annonces conformes et des annonces en quarantaine.
6. Exportation des résultats.
7. Génération du rapport de qualité.

## 8. Règles de nettoyage et de validation

Les données sont soumises à plusieurs contrôles afin de détecter les anomalies.

| Champ ou contrôle | Règle appliquée |
|---|---|
| Identifiant | L'identifiant source doit être renseigné |
| Prix | Le prix doit être numérique et strictement positif |
| Surface | La surface doit être numérique et strictement positive |
| Date | La date doit pouvoir être interprétée correctement |
| Date de vente | Une annonce indiquée comme vendue ne doit pas avoir une date future |
| Surface inhabituelle | Une surface inférieure à 5 m² ou supérieure à 2 000 m² génère un avertissement |
| Prix inhabituel | Un prix inférieur à 100 000 FCFA ou supérieur à 2 milliards FCFA génère un avertissement |

Les valeurs présentant des formats différents sont normalisées lorsque cela est possible.

Exemples :

| Valeur initiale | Valeur normalisée |
|---|---|
| `26 620 000` | `26620000` |
| `57.62 millions` | `57620000` |
| `75,5` | `75.5` |
| `15/03/2024` | `2024-03-15` |

### Gestion des anomalies

Deux catégories de résultats sont produites :

- **Annonces conformes :** annonces qui satisfont les règles de validation obligatoires.
- **Annonces en quarantaine :** annonces qui présentent une anomalie bloquante et nécessitent une vérification ou une correction.

Les avertissements permettent de signaler des valeurs inhabituelles sans nécessairement rejeter l'annonce.

## 9. Résultats du traitement

Le pipeline a été exécuté sur un ensemble de **3 184 annonces** provenant des cinq sources.

Les résultats obtenus sont les suivants :

| Indicateur | Résultat |
|---|---:|
| Nombre total d'annonces | 3 184 |
| Annonces conformes | 2 997 |
| Annonces en quarantaine | 187 |
| Annonces avec avertissements | 50 |
| Taux de conservation | 94,13 % |
| Taux de quarantaine | 5,87 % |
| Annonces complètes | 3 004 |
| Taux de complétude | 94,35 % |
| Annonces incomplètes | 180 |

**Interprétation :**

Sur les 3 184 annonces initiales, 2 997 ont satisfait aux règles de validation et ont été conservées dans le jeu de données conforme. Les 187 autres ont été isolées dans le fichier de quarantaine pour permettre leur vérification.

Le taux de conservation de 94,13 % indique que la grande majorité des annonces a pu être exploitée après traitement.

Le taux de complétude est un indicateur distinct : il repose notamment sur la disponibilité du prix et de la surface. Il ne correspond donc pas exactement au taux de conformité global.

## 10. Analyse exploratoire des données (EDA)

Une analyse exploratoire a été réalisée dans le notebook `notebooks/eda_analyse_exploratoire.ipynb`, à partir des fichiers conformes et en quarantaine.

Elle permet d'examiner la structure du jeu de données, les valeurs manquantes, les doublons, les distributions et les principales caractéristiques des annonces.

### 10.1 Analyse des prix et des surfaces

Sur les 2 997 annonces conformes :

| Indicateur | Prix | Surface |
|---|---:|---:|
| Nombre de valeurs | 2 997 | 2 997 |
| Moyenne | 88 729 760 | 240,73 |
| Médiane | 59 633 000 | 147 |
| Minimum | 40 000 | 10,2 |
| Maximum | 567 559 000 | 1 494,8 |

Les prix et les surfaces présentent une dispersion importante. La médiane est donc utile pour compléter l'interprétation des moyennes, qui peuvent être influencées par les valeurs extrêmes.

### 10.2 Prix au mètre carré

Un indicateur de prix au mètre carré a été calculé :

```python
df["prix_m2"] = df["prix"] / df["surface"]
```

Les principaux résultats sont :

| Indicateur | Prix au m² |
|---|---:|
| Moyenne | 624 573 |
| Médiane | 531 068 |
| Minimum | 37,28 |
| Maximum | 4 603 188 |

**Attention :** ces résultats doivent être interprétés avec prudence. Une grande partie des annonces ne dispose pas d'une devise ou d'une périodicité clairement renseignée. Les prix de vente et les loyers mensuels ne doivent pas être comparés directement.

### 10.3 Répartition géographique

Les villes les plus représentées dans le jeu de données comprennent :

| Ville | Nombre d'annonces |
|---|---:|
| Kébémer | 91 |
| Kanel | 83 |
| Koungheul | 82 |
| Ourossogui | 80 |
| Kaffrine | 79 |
| Médina Yoro Foulah | 79 |
| Goudomp | 79 |
| Bounkiling | 79 |
| Linguère | 78 |
| Bignona | 78 |

Cette répartition montre que les données couvrent plusieurs localités du Sénégal. Elle ne représente toutefois pas nécessairement le volume réel du marché immobilier dans chacune de ces villes : elle dépend aussi des sources collectées.

### 10.4 Répartition par catégorie de bien

Un regroupement exploratoire des catégories, après suppression des espaces superflus et uniformisation de la casse, donne notamment :

| Catégorie | Nombre d'annonces |
|---|---:|
| Appartement | 706 |
| Maison | 634 |
| Villa | 515 |
| Terrain | 440 |
| Studio | 357 |
| Chambre | 181 |
| Local commercial | 159 |
| Appart | 5 |

La présence de plusieurs écritures pour une même catégorie montre l'intérêt d'un référentiel de catégories et d'une normalisation cohérente.

Ce regroupement est une opération d'analyse exploratoire. Il ne signifie pas nécessairement que les valeurs du fichier final ont toutes été corrigées.

### 10.5 Répartition par source

| Source | Nombre d'annonces |
|---|---:|
| Plateforme | 863 |
| Agence | 631 |
| Particuliers | 595 |
| Historique | 518 |
| Notaires | 390 |

La plateforme immobilière est la source la plus représentée dans le jeu de données conforme.

### 10.6 Répartition par type de transaction

| Type de transaction | Nombre | Pourcentage |
|---|---:|---:|
| Vente | 1 111 | 37,07 % |
| Location | 347 | 11,58 % |
| Non renseigné | 1 539 | 51,35 % |

La proportion importante de types de transaction non renseignés constitue une limite pour les analyses qui cherchent à distinguer les ventes des locations.

### 10.7 Analyse de la devise et de la périodicité

| Valeur | Nombre | Pourcentage |
|---|---:|---:|
| FCFA | 688 | 22,96 % |
| FCFA/mois | 175 | 5,84 % |
| Non renseignée | 2 134 | 71,20 % |

La valeur `FCFA/mois` contient une information de périodicité. Il serait donc pertinent, dans une amélioration future, de séparer la devise et la périodicité dans deux colonnes distinctes.

### 10.8 Analyse des doublons

L'analyse a mis en évidence :

- 14 lignes entièrement dupliquées dans les annonces conformes ;
- 1 ligne entièrement dupliquée dans les annonces en quarantaine ;
- 14 identifiants sources répétés dans les annonces conformes.

Ces éléments doivent être examinés avant toute suppression automatique. Deux annonces possédant certaines informations similaires peuvent correspondre à des biens différents ou à des publications distinctes.

## 11. Fichiers générés

Après l'exécution du pipeline, trois fichiers principaux sont disponibles dans `data/processed/`.

| Fichier | Description |
|---|---|
| `annonces_conformes.csv` | Contient les annonces ayant passé les contrôles obligatoires |
| `annonces_quarantaine.csv` | Contient les annonces présentant des anomalies bloquantes |
| `rapport_qualite.json` | Contient les indicateurs et statistiques de qualité du traitement |

Ces fichiers constituent les résultats principaux du processus de traitement.

## 12. Limites identifiées

L'analyse a permis d'identifier plusieurs limites dans les données :

- Une proportion importante de types de transaction n'est pas renseignée.
- La devise ou la périodicité du prix est absente pour de nombreuses annonces.
- Certaines catégories de biens sont écrites de plusieurs manières.
- Des doublons sont présents dans le jeu de données.
- Certaines dates ou valeurs numériques sont incorrectes.
- La couverture géographique et le nombre d'annonces dépendent des sources disponibles.

Ces limites doivent être prises en compte lors de l'interprétation des résultats.

## 13. Perspectives d'amélioration

Plusieurs évolutions pourraient être envisagées :

1. Améliorer la normalisation des catégories à partir du référentiel existant.
2. Séparer la devise et la périodicité du prix.
3. Renforcer le contrôle des identifiants pour faciliter la détection des doublons.
4. Enrichir les référentiels géographiques.
5. Ajouter des visualisations pour faciliter l'analyse des prix, des surfaces et des répartitions géographiques.
6. Améliorer le suivi des anomalies à partir du rapport de qualité.
7. Mettre en place des tests automatisés supplémentaires pour sécuriser les traitements.

## 14. Conclusion

Le projet **ImmoAnalyse** met en place un processus structuré de collecte, de préparation, de normalisation et de validation de données immobilières provenant de plusieurs sources.

L'exécution du pipeline a permis de traiter 3 184 annonces, d'en conserver 2 997 comme annonces conformes et d'isoler 187 annonces en quarantaine.

L'analyse exploratoire a également permis d'identifier les principales caractéristiques du jeu de données, les valeurs manquantes, les doublons et les limites qui peuvent influencer les analyses.

Ce travail constitue une première étape vers la constitution d'un jeu de données immobilier plus fiable, exploitable pour des analyses statistiques, des tableaux de bord et des projets d'aide à la décision.

---

**Projet :** ImmoAnalyse  
**Langage :** Python  
**Domaine :** Traitement et analyse de données immobilières