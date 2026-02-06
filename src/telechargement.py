"""
Téléchargement HTTP (HTML et binaire).
- Téléchargement du HTML d'une page.
- Téléchargement binaire (pour les images).
"""

from typing import Optional
import requests

HEADERS = {"User-Agent": "books-scraper/1.0"}

def telecharger_page(url: str, timeout: int = 10, user_agent: Optional[str] = None) -> str:
    """
    Télécharge le HTML d'une page et retourne le texte.

    Args:
        url: URL de la page.
        timeout: Délai maximum (secondes).
        user_agent: Pour personnaliser l'agent utilisateur si besoin.

    Retour:
        HTML de la page sous forme de chaîne.
    """
    headers = HEADERS.copy()
    if user_agent:
        headers["User-Agent"] = user_agent

    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def telecharger_binaire(url: str, timeout: int = 10, user_agent: Optional[str] = None) -> bytes:
    """
    Télécharge un contenu binaire (ex: image) et retourne les octets.

    Args:
        url: URL du contenu (ex: image).
        timeout: Délai maximum (secondes).
        user_agent: Pour personnaliser l'agent utilisateur.

    Retour:
        Contenu binaire (octets).
    """
    headers = HEADERS.copy()
    if user_agent:
        headers["User-Agent"] = user_agent

    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.content