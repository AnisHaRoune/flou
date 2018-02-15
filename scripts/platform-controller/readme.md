# Contrôleur de la plateforme

## Description
Cet outil communique avec le pilote de la plateforme grâce au port série.

## Configuration du GPIO Raspberry Pi
Pour une communication faite avec le GPIO du Raspberry Pi, le port série doit être configuré d'une certaine manière pour communiquer avec le pilote. La [procédure](https://github.com/steven-pigeon/flou/wiki/Communication-s%C3%A9rie) se trouve dans le wiki.

## Utilisation
Sous Linux :
```bash
./platform-controller.sh /dev/ttyUSB0
```
Sous Windows:
```bash
./platform-controller.sh COM3
```
Une fois l'outils démarré, il suffit de taper les commandes du pilote et le résultat sera affiché en temps réel. CTRL-C termine l'éxecution.

### Commandes
Voici le résultat de la command "h" (help) envoyé au pilote :
```
Montage specifications:  
There is 6400 microsteps by turn.  
Each turn moves the platform by 2 mm.  
Each step moves the platform by 0.3125 um.   
  
Stepper motor control commands:  
{command_char}[[sign]{value}[unit]]{end_char}    
[[sign]{value}[unit]] may be omitted if {command_char} do not need it.    
[[sign]{value}[unit]] may be omitted if {command_char} is used as a getter-setter.  
[sign] is optional.  
[unit] is only used with the m {command_char}.  
Buffer size is 16 character.  
h   : Print the help  
s   : Step the motor  
t   : Turn the lead screw  
m   : Move the platform in [unity]. May be cm, mm or um  
d   : Set the delay in microsecond between each half step. Default is 10  
f   : Move the platform to the front  
b   : Move the platform to the back  
x   : Stop the current action  
\n  : Ending character   
  
Example: s400  
Move forward 400 steps.  
  
Example: m-18.5cm  
Move backward 18.5 cm.  
  
Example: d39  
Set delay at 39 microsecond.  
  
Example: d  
Return delay value.
```