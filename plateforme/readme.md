# Montage specifications
Each turn moves the platform by 2 mm.  
There is 6400 steps by turn.  
Each step moves the platform by 0.3125 um.  
# Platform control
## Stepper motor control commands
{command_char}[[sign]{value}[unit]]{end_char}  
[[sign]{value}[unit]] may be omitted if {command_char} do not need it.  
[[sign]{value}[unit]] may be omitted if {command_char} is used as a getter-setter.  
[sign] is optional.  
[unit] is only used with the m {command_char}.  
Buffer size is 16 character.  
* s   : Steps the motor  
* t   : Turns the lead screw  
* m   : Moves the platform in [unity]. May be cm, mm or um  
* d   : Sets the delay in microsecond between each half step. Default is 10  
* f   : Moves the platform to the front  
* b   : Moves the platform to the back  
* x   : Stops the current action  
* \n  : Ending character  
### Exemples
`s400`      : Move forward 400 steps.  
`m-18.5cm`  : Move backward 18.5 cm.  
`d39`       : Set delay at 39 microsecond.  
`d`         : Return delay value.  
