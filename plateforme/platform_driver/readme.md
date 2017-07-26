# Pilote de plateforme

## Description
Ce projet est le code qui pilote le moteur pour la plateforme. Les spécifications détaillées du [circuit](https://www.github.com) et de la [plateforme](https://github.com/steven-pigeon/flou/wiki/Plans-de-la-plateforme) sont disponible sur le wiki.

## Communication
Série //TODO: détails (wiki?)

## Utilisation
Voici le résultat de la command "h" (help) du pilote :  
  
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