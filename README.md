# Books To Scrape – Scraper Python

Scraper pédagogique pour extraire des informations du site public de démonstration : https://books.toscrape.com/.

## Fonctions principales
- Récupère les **catégories**.
- Parcourt les pages d’une catégorie (démo : 1 page / catégorie ; complet : toute la pagination).
- Extrait : **titre**, **prix**, **stock**, **note** (convertie en **étoiles ★**), **URL image**, **catégorie**.
- Télécharge les **images**.
- Génère **un CSV par catégorie** dans `data/<Catégorie>/books.csv`.
- Affiche des **barres de progression** pour les téléchargements.

## Prérequis
- **Python 3.10+**
- Accès Internet

## Installation
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
