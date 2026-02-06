# Books To Scrape – Scraper Python

Projet 2 OPC permettant d'extraire les informations du site https://books.toscrape.com/.

Ce que fait le programme :
- Récupère toutes les catégories.
- Parcourt toutes les pages de chaque catégorie.
- Extrait les livres (titre, prix, note, stock, image, catégorie).
- Convertit la note en étoiles (★☆☆☆☆ → ★★★★★).
- Récupère le stock depuis la page détail.
- Télécharge les images.
- Génère un CSV par catégorie.
- Affiche une barre de progression pour le téléchargement.

Technologies utilisées :
- Python
- Requests
- BeautifulSoup
- tqdm

Structure générale :
- `demo.py` : exécution rapide (1 seule catégorie).
- `main.py` : exécution complète (toutes les catégories).
- `src/telechargement.py` : téléchargement HTML / images.
- `src/categorie.py` : extraction des catégories.
- `src/livre.py` : extraction des données livres + stock + correction des URLs.
- `src/enregistrement.py` : création CSV et sauvegarde des images.
- `data/` : résultats générés.

Installation :
1. Créer un environnement virtuel.
2. Installer les dépendances.
3. Lancer la démo ou l’exécution complète.

```bash
python -m venv .venv
source .venv/bin/activate         # Windows : .venv\Scripts\activate
pip install -r requirements.txt