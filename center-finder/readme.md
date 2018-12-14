# Utilitaire pour trouver le centre d'un laser

## Description
Quelques outils pour trouver le centre d'un laser dans une image ou dans une collection d'images.

## Installation
### Dépendances
* Python 3
* Les dépendances listées dans le fichier "requirements.txt"

## Utilisation
### center-finder.py
```bash
usage: center-finder.py [-h] [--threshold_method {min,mean,median,log}]
                        [-z0 Z0] [--debug]
                        filepath {centroid,circle,diffraction,isquare,euler}

positional arguments:
  filepath
  {centroid,circle,diffraction,isquare,euler}

optional arguments:
  -h, --help            show this help message and exit
  --threshold_method {min,mean,median,log}, -t {min,mean,median,log}
  -z0 Z0
  --debug, -d
```
La sortie est une coordonnée cartésienne 2D sous la forme x;y.
* filepath est le chemin vers l'image contenant le laser.
* {centroid,circle,diffraction,isquare,euler} est la méthode à utilisée pour trouver le laser.
* threshold_method est la méthode utilisé pour nettoyer le bruit.
* Si threshold_method n'est pas utilisé, la valeur de z0 sera utilisée pour éliminer le bruit. Si z0 n'est pas spécifié non plus, le bruit sera gardé.
* debug permet d'afficher des images au long du processus pour visualer le centre et afficher des informations supplémentaires lors du débogage.

Exemple d'utilisation :
```bash
python center-finder.py test-data/laser.bmp diffraction -t log
147.78168193964166;193.97345372122828
```
Exemple d'image de débogage :    
![centre d'un laser](https://github.com/steven-pigeon/flou/blob/master/center-finder/centerfinder-debug.png "Centre d'un laser")

### center-finder-plotter.sh
```bash
./center-finder-plotter.sh method threshold_method images_dir
```
Ce script va passer en ordre sur chaque image dans le dossier "images_dir" et appliquer le script "center-finder.py" sur chacune d'elles.
Les résultats sont compilés dans un fichier CSV. Une ligne est formattée tel que suit :
```ID;PATH;X;Y```
Exemple d'utilisation :
```bash
./center-finder-plotter.sh isquare mean images/
```
Cette commande créera le fichier "images_isquare_mean.csv".