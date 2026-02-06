"""
Fonctions liées aux catégories de livres.
- Extraction des catégories depuis la page d'accueil.
"""

from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extraire_categories(html_index, url_base):
    """
    Extrait la liste des catégories.

    Args:
        html_index: HTML de la page d'accueil.
        url_base: URL de base du site.

    Retour:
        Liste de dictionnaires : {"nom": <Nom>, "url": <URL absolue>}
    """
    soup = BeautifulSoup(html_index, "lxml")
    elements = soup.select("ul.nav-list li ul li a")

    categories = []
    for lien in elements:
        nom = lien.get_text(strip=True)
        url = urljoin(url_base, lien.get("href"))
        categories.append({"nom": nom, "url": url})

    return categories
