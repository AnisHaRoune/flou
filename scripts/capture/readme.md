# Outils de captures

## Description
Cet outil permet de prendre des photos à interval régulier sur une plage de distance, grâce à la plateforme.

## Dépendance
```bash
apt-get install fswebcam
```

## Utilisation
Paramètres obligatoires :
1. port de communication
2. nombre de photo
3. distance des intervales
4. Unité de distance
5. Nom de l'image
### Exemple
```bash
./capture.sh /dev/ttyUSB0 3 -2 mm exemple
```
Prends 3 photos à tout les 2 mm (vers l'arrière, puisque -2 est négatif). Les noms des images seront "exemple0.jpg", "exemple1.jpg" et "exemple2.jpg" et ils seront dans le dossier "captures", créé au besoin par l'utilitaire.