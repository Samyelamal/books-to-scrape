
# Fonction qui télécharge une page web à partir de son URL.

import requests

def telecharger_page(url):
    """Télécharge le contenu HTML d'une page web et retourne le texte."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text
