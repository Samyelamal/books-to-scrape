"""
Exécution complète :
- Toutes les catégories.
- Toute la pagination.
- CSV et images par catégorie dans data/.
"""

import json
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from src.telechargement import telecharger_page
from src.categorie import extraire_categories
from src.livre import extraire_livres
from src.enregistrement import enregistrer_csv, enregistrer_image
from tqdm import tqdm


def lister_pages_categorie(url_categorie, timeout):
    """
    Suit la pagination d'une catégorie et retourne la liste des URLs de pages.
    """
    pages = []
    url_courante = url_categorie

    while True:
        pages.append(url_courante)
        html = telecharger_page(url_courante, timeout=timeout)
        soup = BeautifulSoup(html, "lxml")

        next_a = soup.select_one("li.next a")
        if not next_a:
            break
        url_courante = urljoin(url_courante, next_a.get("href"))

    return pages


def main():
    # Charger la configuration
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base = cfg["url_base"]
    timeout = cfg.get("timeout", 10)

    # Page d'accueil et catégories
    index_html = telecharger_page(urljoin(base, "index.html"), timeout=timeout)
    categories = extraire_categories(index_html, base)

    for cat in categories:
        nom_cat, url_cat = cat["nom"], cat["url"]
        print(f"\n=== Catégorie : {nom_cat} ===")

        # Lister toutes les pages de la catégorie
        pages = lister_pages_categorie(url_cat, timeout)

        # Extraire tous les livres de la catégorie
        tous_les_livres = []
        for p_url in pages:
            page_html = telecharger_page(p_url, timeout=timeout)
            livres = extraire_livres(page_html, base, nom_cat)
            tous_les_livres.extend(livres)

        # Sauvegarde CSV
        dossier_cat = os.path.join("data", nom_cat)
        chemin_csv = os.path.join(dossier_cat, "books.csv")
        enregistrer_csv(tous_les_livres, chemin_csv)

        # Sauvegarde images (avec barre de progression)
        for i, livre in enumerate(tqdm(tous_les_livres, desc=f"Téléchargement images ({nom_cat})"), start=1):
            nom_img = f"book_{i}.jpg"
            try:
                enregistrer_image(livre.url_image, dossier_cat, nom_img)
            except Exception as e:
                print(f"image ignorée ({livre.url_image}) : {e}")

        print(f"{len(tous_les_livres)} livres — CSV : {chemin_csv}")


if __name__ == "__main__":
    main()