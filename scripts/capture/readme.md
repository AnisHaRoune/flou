# Outils de captures

## Description
Cet outil permet de prendre des photos à interval régulier sur une plage de distance, grâce à la plateforme.

## Dépendance sous Linux
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
Sous Linux :
```bash
./capture.sh /dev/ttyUSB0 1 -2 mm 3 exemple
```
Sous Windows:
```powershell
./capture.ps1 COM3 2 -5 mm 2 exemple
```
Prends 2 photos à tout les 5 mm (vers l'arrière, puisque -2 est négatif), et répète cette opération 2 fois. Les noms des images seront "00000000-exemple-0mm-0.png", "00000001-exemple-0mm-1.png", "00000002-exemple-5mm-0.png" et "00000003-exemple-5mm-1.png" et ils seront dans le dossier "captures", créé au besoin par l'utilitaire.