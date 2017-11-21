# Outils de calibration de la caméra

## Description
Affiche une vue de la camera avec la meilleur resolution possible et un viseur en son centre.

## Installation
### Dépendances
```apt-get install libboost-all-dev libopencv-dev```
//TODO: Il manque sûrement beaucoup d'information ici (exemple: CMake).
### Compilation
```bash
cmake .
make
```  

## Utilisation
```bash
./calibration
```
La touche ESPACE allume ou eteint le viseur de calibration.  
Les flèches HAUT, BAS, GAUCHE et DROITE permettent d'ajuster la position verticale et horizontale du viseur. Le viseur commence toujours au centre.  
La touche ESC permet de quitter.
###gnuplot
La touche ENTREE creer un fichier "plot/points.data".
Ce fichier est une liste de la valeur de tous les pixels sur la ligne horizontale au centre du rectangle du viseur.
Ce fichier est utilisable par gnuplot. Le script plot/plot-roi.plt genere un graphique et est utilise tel que suit :  
```bash
gnuplot plot/plot-roi.plt -p
```
Cette commande peut etre repetee a chaque fois que le fichier points.data est regenere.