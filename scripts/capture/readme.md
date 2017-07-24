# Outils de captures

## Description
Cet outil permet de prendre des photos à interval régulier sur une plage de distance, grâce à la plateforme.

## Utilisation
Paramètres :
1. nombre de photo
2. distance des intervales
3. Unité de distance
4. Nom de l'image
### Exemple
```bash
./capture.sh 3 -2 mm exemple
```
Prends 3 photos à tout les 2 mm (vers l'arrière, puisque -2 est négatif). Les noms des images seront "exemple0.jpg", "exemple1.jpg" et "exemple2.jpg" et ils seront dans le dossier "captures", créé au besoin par l'utilitaire.