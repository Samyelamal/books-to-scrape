"""
Objet Livre et extraction depuis une page de catégorie.

Données récupérées :
- Titre
- Prix (float)
- Note (1 à 5)
- URL de l'image
- Catégorie
- Stock disponible
- UPC
"""

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.telechargement import telecharger_page


CONVERSION_NOTES = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


@dataclass
class Livre:
    titre: str
    prix: float
    note: int
    url_image: str
    categorie: str
    stock: int
    upc: str


def _prix_vers_float(prix_str: str) -> float:
    """Convertit un prix '£51.77' en 51.77 (float)."""
    return float(prix_str.replace("Â", "").replace("£", "").strip())


def _note_depuis_classes(classes) -> int:
    """Récupère la note via les classes CSS (ex: 'Three')."""
    for c in classes:
        if c in CONVERSION_NOTES:
            return CONVERSION_NOTES[c]
    return 0


def _normaliser_href_detail(href: str) -> str:
    """
    Corrige les href relatifs de BooksToScrape pour pointer vers 'catalogue/...'
    Exemple : '../../../titre_123/index.html' -> 'catalogue/titre_123/index.html'
    """
    if href.startswith("../../../"):
        return "catalogue/" + href.replace("../../../", "")
    if href.startswith("../../"):
        return "catalogue/" + href.replace("../../", "")
    return href


def extraire_stock(html_detail: str) -> int:
    """
    Extrait la quantité disponible depuis la page détail.
    Exemple : 'In stock (22 available)' -> 22
    Retourne 0 si non trouvé.
    """
    soup = BeautifulSoup(html_detail, "lxml")
    bloc = soup.find("p", class_="instock availability")
    if not bloc:
        return 0
    txt = bloc.get_text(strip=True)
    m = re.search(r"\((\d+)\s+available\)", txt)
    return int(m.group(1)) if m else 0


def extraire_upc(html_detail: str) -> str:
    """
    Extrait le numéro UPC depuis la page détail.
    Retourne '' si non trouvé.
    """
    soup = BeautifulSoup(html_detail, "lxml")
    table = soup.find("table", class_="table table-striped")
    if not table:
        return ""

    # L'UPC est dans la première ligne du tableau d'informations produit
    first_row = table.find("tr")
    if not first_row:
        return ""

    upc_cell = first_row.find("td")
    return upc_cell.get_text(strip=True) if upc_cell else ""


def extraire_livres(html_page: str, url_base: str, nom_categorie: str, timeout: int = 10):
    """
    Extrait tous les livres d'une page catégorie.

    Le stock et l'UPC ne figurent que sur la page détail de chaque livre,
    qui est donc téléchargée en plus de la page catégorie.
    """
    soup = BeautifulSoup(html_page, "lxml")
    livres = []

    for produit in soup.select("article.product_pod"):
        titre = produit.h3.a.get("title", "").strip()

        prix_str = produit.select_one(".price_color").get_text(strip=True)
        prix = _prix_vers_float(prix_str)

        rating_tag = produit.select_one(".star-rating")
        classes_note = rating_tag["class"] if rating_tag and rating_tag.has_attr("class") else []
        note = _note_depuis_classes(classes_note)

        url_image = urljoin(url_base, produit.img.get("src", ""))

        url_detail_rel = _normaliser_href_detail(produit.h3.a.get("href", ""))
        url_detail = urljoin(url_base, url_detail_rel)

        stock = 0
        upc = ""
        try:
            html_detail = telecharger_page(url_detail, timeout=timeout)
            stock = extraire_stock(html_detail)
            upc = extraire_upc(html_detail)
        except Exception:
            # Une page détail inaccessible ne doit pas interrompre toute la catégorie
            pass

        livres.append(
            Livre(
                titre=titre,
                prix=prix,
                note=note,
                url_image=url_image,
                categorie=nom_categorie,
                stock=stock,
                upc=upc,
            )
        )

    return livres
