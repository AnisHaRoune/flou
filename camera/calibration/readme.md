# Outils de calibration de la caméra

## Description
Affiche une vue de la camera avec la meilleur resolution possible et un viseur en son centre.

## Installation
### Dépendances
```bash
sudo apt-get install libopencv-dev
sudo apt-get install cmake
sudo apt-get install gnuplot
```
### Compilation
```bash
cmake .
make
```  

## Utilisation
```bash
./calibration
```
La touche ESPACE allume ou éteint le viseur de calibration.  
Les flèches HAUT, BAS, GAUCHE et DROITE permettent d'ajuster la position verticale et horizontale du viseur. Le viseur commence toujours au centre.  
La touche ESC permet de quitter.
### gnuplot
La touche ENTREE créer un fichier "points.data".
Ce fichier est une liste de la valeur de tous les pixels sur la ligne horizontale au centre du rectangle du viseur.
Ce fichier est utilisable par gnuplot. Le script plot-roi.plt génère un graphique et est utilisé tel que suit :  
```bash
gnuplot plot-roi.plt -p
```
Cette commande peut etre répétée à chaque fois que le fichier points.data est regénéré.