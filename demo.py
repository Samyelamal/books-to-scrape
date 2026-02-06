"""
Démo rapide :
- Récupère la 1re catégorie.
- Sauvegarde un CSV.
- Télécharge les images.
"""

import json
import os
from urllib.parse import urljoin
from tqdm import tqdm

from src.telechargement import telecharger_page
from src.categorie import extraire_categories
from src.livre import extraire_livres
from src.enregistrement import enregistrer_csv, enregistrer_image


def main():
    # Charger la configuration
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base = cfg["url_base"]
    timeout = cfg.get("timeout", 10)
    note_format = cfg.get("note_format", "all")

    # Accueil
    html_index = telecharger_page(urljoin(base, "index.html"), timeout=timeout)

    # Catégories
    categories = extraire_categories(html_index, base)
    categorie = categories[0]  # 1re catégorie
    nom_cat, url_cat = categorie["nom"], categorie["url"]

    # Page de la catégorie
    cat_html = telecharger_page(url_cat, timeout=timeout)

    # Livres de cette page uniquement
    livres = extraire_livres(cat_html, base, nom_cat, timeout=timeout)

    # Dossier catégorie
    dossier_cat = os.path.join("data", nom_cat)
    chemin_csv = os.path.join(dossier_cat, "books.csv")

    # Sauvegarde CSV (format de note configurable)
    enregistrer_csv(livres, chemin_csv)

    # Télécharger toutes les images (avec barre de progression)
    for i, livre in enumerate(tqdm(livres, desc=f"Téléchargement images ({nom_cat})"), start=1):
        enregistrer_image(livre.url_image, dossier_cat, f"book_{i}.jpg")

    print(f"Démo OK : {len(livres)} livres trouvés dans '{nom_cat}'.")
    print(f"CSV : {chemin_csv}")
    print(f"Images : data/{nom_cat}/images/")


if __name__ == "__main__":
    main()