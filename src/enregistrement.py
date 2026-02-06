"""
Enregistrement local :
- Création des dossiers par catégorie.
- Sauvegarde CSV.
- Téléchargement des images.
"""

import os
import csv
from src.telechargement import telecharger_binaire


def creer_dossier(chemin):
    """Crée le dossier s'il n'existe pas."""
    os.makedirs(chemin, exist_ok=True)


def enregistrer_csv(livres, chemin_fichier):
    """
    Enregistre une liste de livres dans un CSV.

    Colonnes :
    - titre
    - prix
    - note
    - url_image
    - categorie
    """
    creer_dossier(os.path.dirname(chemin_fichier))

    with open(chemin_fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["titre", "prix", "note", "url_image", "categorie"])

        for livre in livres:
            writer.writerow([
                livre.titre,
                livre.prix,
                livre.note,
                livre.url_image,
                livre.categorie,
            ])


def enregistrer_image(url_image, dossier_categorie, nom_fichier):
    """
    Télécharge et enregistre une image dans 'data/<cat>/images/<nom_fichier>'.

    Retour:
        Chemin complet de l'image enregistrée.
    """
    images_dir = os.path.join(dossier_categorie, "images")
    creer_dossier(images_dir)

    chemin_image = os.path.join(images_dir, nom_fichier)
    contenu = telecharger_binaire(url_image)

    with open(chemin_image, "wb") as f:
        f.write(contenu)

    return chemin_image
