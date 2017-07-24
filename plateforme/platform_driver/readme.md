# Platform Driver

## Description
Ce projet est le code qui pilote le moteur pour la plateforme. Les spécifications détaillées du [circuit](https://www.github.com) et de la [plateforme](https://www.github.com) sont disponible sur le wiki.

##Communication
Série //TODO: détails

## Commandes
Voici le résultat de la command "h" (help) du pilote :    
Montage specifications:  
Each turn moves the platform by 2 mm.  
There is 6400 steps by turn.  
Each step moves the platform by 0.3125 um.  
  
Stepper motor control commands:  
{command_char}[[sign]{value}[unit]]{end_char}    
[[sign]{value}[unit]] may be omitted if {command_char} do not need it.    
[[sign]{value}[unit]] may be omitted if {command_char} is used as a getter-setter.  
[sign] is optional.  
[unit] is only used with the m {command_char}.  
Buffer size is 16 character.  
s   : Steps the motor  
t   : Turns the lead screw  
m   : Moves the platform in [unity]. May be cm, mm or um  
d   : Sets the delay in microsecond between each half step. Default is 10  
f   : Moves the platform to the front  
b   : Moves the platform to the back  
x   : Stops the current action  
\n  : Ending character  
  
Example: s400  
Move forward 400 steps.  
  
Example: m-18.5cm  
Move backward 18.5 cm.  
  
Example: d39  
Set delay at 39 microsecond.  
  
Example: d  
Return delay value.  
