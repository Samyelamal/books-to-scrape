"""
Enregistrement local :
- Création des dossiers par catégorie.
- Sauvegarde CSV (note au format étoiles uniquement).
- Téléchargement des images.
"""

import os
import csv
from src.telechargement import telecharger_binaire


def creer_dossier(chemin: str):
    """Crée le dossier s'il n'existe pas."""
    os.makedirs(chemin, exist_ok=True)


def _note_en_etoiles(note: int) -> str:
    """Convertit une note 0..5 en étoiles (ex: ★★★☆☆)."""
    try:
        n = int(note)
    except Exception:
        n = 0
    n = max(0, min(5, n))
    return "★" * n + "☆" * (5 - n)



def enregistrer_csv(livres, chemin_fichier: str):
    """
    Enregistre une liste de livres dans un CSV.

    Colonnes :
    - titre
    - prix
    - note_etoiles (★..☆)
    - stock (quantité disponible)
    - url_image
    - categorie
    """
    creer_dossier(os.path.dirname(chemin_fichier))

    with open(chemin_fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow([
            "titre",
            "prix",
            "note_etoiles",
            "stock",
            "url_image",
            "categorie",
        ])

        # Lignes
        for livre in livres:
            writer.writerow([
                livre.titre,
                livre.prix,
                _note_en_etoiles(getattr(livre, "note", 0)),
                int(getattr(livre, "stock", 0)),
                livre.url_image,
                livre.categorie,
            ])


def enregistrer_image(url_image: str, dossier_categorie: str, nom_fichier: str):
    """
    Télécharge et enregistre une image dans 'data/<cat>/images/<nom_fichier>'.

    Retour:
        Chemin complet de l'image enregistrée.
    """
    images_dir = os.path.join(dossier_categorie, "images")
    creer_dossier(images_dir)

    chemin_image = os.path.join(images_dir, nom_fichier)
    contenu = telecharger_binaire(url_image)