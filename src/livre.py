"""
Objet Livre et extraction depuis une page de catégorie.
- Titre.
- Prix (float, sans symbole £).
- Note (int, 1 à 5).
- URL image.
"""

from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Conversion texte -> note
CONVERSION_NOTES = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

@dataclass
class Livre:
    """Représente un livre."""
    titre: str
    prix: float
    note: int
    url_image: str
    categorie: str


def _prix_vers_float(prix_str):
    """Convertit un prix '£51.77' en 51.77 (float)."""
    # Certains environnements ajoutent un caractère 'Â' avant '£', on le retire au cas où.
    return float(prix_str.replace("Â", "").replace("£", "").strip())


def _note_depuis_classes(classes):
    """Récupère la note via les classes CSS (ex: 'Three')."""
    for c in classes:
        if c in CONVERSION_NOTES:
            return CONVERSION_NOTES[c]
    return 0


def extraire_livres(html_page, url_base, nom_categorie):
    """
    Extrait tous les livres présents sur une page de catégorie.

    Args:
        html_page: HTML de la page de catégorie.
        url_base: URL de base du site.
        nom_categorie: Nom de la catégorie (pour renseigner l'objet Livre).

    Retour:
        Liste d'objets Livre.
    """
    soup = BeautifulSoup(html_page, "lxml")
    livres = []

    for produit in soup.select("article.product_pod"):
        # Titre
        titre = produit.h3.a.get("title", "").strip()

        # Prix (float)
        prix_str = produit.select_one(".price_color").get_text(strip=True)
        prix = _prix_vers_float(prix_str)

        # Note (int)
        classes_note = produit.select_one(".star-rating")["class"]
        note = _note_depuis_classes(classes_note)

        # URL image absolue
        img_rel = produit.img.get("src", "")
        url_image = urljoin(url_base, img_rel)

        livres.append(
            Livre(
                titre=titre,
                prix=prix,
                note=note,
                url_image=url_image,
                categorie=nom_categorie,
            )
        )

    return livres