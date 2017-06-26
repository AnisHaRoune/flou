#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <Arduino.h>

#define STP 2
#define DIR 3
#define MS1 4
#define MS2 5
#define MS3 6
#define EN  7
#define FRONT_SWITCH  19
#define BACK_SWITCH   18

#define FORWARD HIGH
#define BACKWARD LOW
#define BUFFER_SIZE 16
#define HELP_CHAR                 'h'
#define FORWARD_CALIBRATION_CHAR  'f'
#define BACKWARD_CALIBRATION_CHAR 'b'
#define STEP_CHAR                 's'
#define TURN_CHAR                 't'
#define MOVE_CHAR                 'm'
#define CM_CHAR                   'c'
#define MM_CHAR                   'm'
#define UM_CHAR                   'u'
#define DELAY_CHAR                'd'
#define SOFT_STOP_CHAR            'x'
#define END_CHAR                  '\n'
#define STEP_BY_TURN 6400
#define MM_BY_TURN 2

unsigned int get_speed();
void set_speed(unsigned int s);
void set_resolution(int resolution);
void calibration(int stepper_direction);
void step_stepper(int32_t steps); //revolver ocelot (revolver ocelot)
void command_output(int32_t steps, int stepper_direction, int reason);
void print_reason(int reason);
int single_step(int stepper_direction);
void motorControlSetup();
void resetBEDPins(); //Reset Big Easy Driver pins to default states
void help();

#endif

