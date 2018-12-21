# Outils de captures

## Description
Cet outil permet de prendre des photos à interval régulier sur une plage de distance, grâce à la plateforme. La version Linux n'est plus maintenue, ni son code, ni sa documentation.

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
### Exemple
Sous Linux :
```bash
./capture.sh /dev/ttyUSB0 1 -2 mm 3 exemple
```
Sous Windows:
```powershell
./capture.ps1 COM3 2 -5 mm 2
```
Prends 2 photos à tout les 5 mm (vers l'arrière, puisque -5 est négatif), et répète cette opération 2 fois. Les noms des images seront "00000000-00000000.png", "00000000-00000001.png", "00005000-00000000.png" et "00005000-00000001.png" et ils seront dans le dossier "captures", créé au besoin par l'utilitaire. Le format de l'image est le suivant : distanceEnMircoMètre-IndexDeCapture.png.