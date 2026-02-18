# Books To Scrape – Scraper Python

Scraper pédagogique pour extraire des informations depuis le site public de démonstration :  
https://books.toscrape.com/

## Fonctionnalités
- Extraction complète des **catégories**
- Parcours de **toute la pagination** (mode complet)
- Extraction des données :
  - Titre
  - Prix (£ → float)
  - Note (convertie en ⭐)
  - Stock disponible
  - URL de l’image
  - Catégorie
  - UPC (identifiant unique)
- Téléchargement automatique des **images**
- Génération d’un **CSV par catégorie** dans `data/<Catégorie>/books.csv`
- Barre de progression via `tqdm`
- Configuration via `config.json`

## Prérequis
- Python **3.10+**
- Connexion Internet

## Installation

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt