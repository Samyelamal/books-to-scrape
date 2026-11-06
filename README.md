# Books To Scrape – Scraper Python

Scraper qui extrait les informations des livres du site de démonstration
[books.toscrape.com](https://books.toscrape.com/) et les enregistre en CSV, catégorie par catégorie.

Projet réalisé dans le cadre du parcours Développeur d'application Python d'OpenClassrooms.

## Fonctionnalités

- Récupération de toutes les catégories depuis la page d'accueil
- Parcours de toute la pagination de chaque catégorie
- Extraction pour chaque livre :
  - titre
  - prix (converti en nombre)
  - note (affichée en étoiles dans le CSV)
  - stock disponible
  - URL de l'image
  - catégorie
  - UPC
- Téléchargement des images de couverture
- Un fichier CSV par catégorie dans `data/<Catégorie>/books.csv`
- Barre de progression avec `tqdm`
- Paramètres regroupés dans `config.json`

## Prérequis

- Python 3.10 ou supérieur
- Une connexion Internet

## Installation

```bash
git clone https://github.com/Samyelamal/books-to-scrape.git
cd books-to-scrape
python -m venv .venv
```

Activer l'environnement virtuel :

```bash
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\Activate.ps1       # Windows PowerShell
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Extraction complète du site (toutes les catégories, toutes les pages) :

```bash
python main.py
```

Version courte pour tester rapidement : seules les premières catégories sont traitées,
et uniquement leur première page.

```bash
python demo.py
```

Les résultats sont écrits dans le dossier `data/` :

```
data/
└── Poetry/
    ├── books.csv
    └── images/
        └── <upc>.jpg
```

## Configuration

| Clé                  | Rôle                                            | Valeur par défaut              |
|----------------------|-------------------------------------------------|--------------------------------|
| `url_base`           | Adresse du site à scraper                       | `https://books.toscrape.com/`  |
| `timeout`            | Délai maximum d'une requête, en secondes        | `10`                           |
| `demo_nb_categories` | Nombre de catégories traitées par `demo.py`     | `5`                            |

## Structure du projet

```
books-to-scrape/
├── src/
│   ├── categorie.py        # Extraction des catégories
│   ├── livre.py            # Modèle Livre et extraction des données
│   ├── telechargement.py   # Requêtes HTTP
│   └── enregistrement.py   # Écriture des CSV et des images
├── config.json
├── demo.py
├── main.py
└── requirements.txt
```

## Qualité du code

Le code respecte la PEP 8 (longueur de ligne maximale : 119), vérifiée avec flake8 :

```bash
pip install flake8
flake8
```
