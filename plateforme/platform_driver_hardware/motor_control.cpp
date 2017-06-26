#include <stdint.h>
#include "motor_control.h"

unsigned int stepper_delay = 10; //in microsecond

unsigned int get_speed()
{
  return stepper_delay;
}

void set_speed(unsigned int s)
{
  stepper_delay = s;
}

void calibration(int stepper_direction)
{
  int32_t i = 0;
  int reason = 0;
  while (!reason)
  {
    reason = single_step(stepper_direction);    
    i++;
  }

  command_output(i, stepper_direction, reason);
}

void step_stepper(int32_t steps)
{
  Serial.print(steps);
  
  int stepper_direction = FORWARD;
  if (steps < 0)
  {
    steps = -steps;
    stepper_direction = BACKWARD;
  }

  int reason;
  int32_t i;
  for(i = 0; i < steps; i++)
  {
    reason = single_step(stepper_direction);

    if (reason)
    {
      break;
    }
  }

  command_output(i, stepper_direction, reason);
}

void command_output(int32_t steps, int stepper_direction, int reason)
{
  if (stepper_direction == BACKWARD)
  {
    steps = -steps;
  }
  
  Serial.print(" ");
  print_reason(reason);
  Serial.print(" ");
  Serial.println(steps);
}

void print_reason(int reason)
{
  switch (reason)
  {
    case SOFT_STOP_CHAR: Serial.print("SOFT_STOP");
      break;
    case FRONT_SWITCH: Serial.print("FRONT_SWITCH");
      break;
    case BACK_SWITCH: Serial.print("BACK_SWITCH");
      break;
    default: Serial.print("DONE");
      break;
  }
}

int single_step(int stepper_direction)
{
  if (Serial.read() == SOFT_STOP_CHAR)
  {
    return SOFT_STOP_CHAR;
  }
  else if ((stepper_direction == FORWARD) && (digitalRead(FRONT_SWITCH)))
  {
    return FRONT_SWITCH;
  }
  else if ((stepper_direction == BACKWARD) && (digitalRead(BACK_SWITCH)))
  {
    return BACK_SWITCH;
  }
  
  digitalWrite(DIR, stepper_direction);
  
  digitalWrite(STP, HIGH);
  delayMicroseconds(stepper_delay);
  digitalWrite(STP, LOW);
  delayMicroseconds(stepper_delay);

  return 0;
}

void motorControlSetup()
{
  pinMode(STP, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(FRONT_SWITCH, INPUT);
  pinMode(BACK_SWITCH, INPUT);
  resetBEDPins();
  set_resolution(HIGH);
}

void resetBEDPins()
{
  digitalWrite(STP, LOW);
  digitalWrite(DIR, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
  digitalWrite(EN, HIGH);
}

void set_resolution(int resolution)
{
  switch (resolution)
  {
    case HIGH:
    {
      digitalWrite(MS1, HIGH); //Pull MS1,MS2, and MS3 high to set logic to 1:16 microstep resolution
      digitalWrite(MS2, HIGH);
      digitalWrite(MS3, HIGH);
    } break;
    case LOW:
    {
      digitalWrite(MS1, LOW); //Pull MS1,MS2, and MS3 low to set logic to 1:1 microstep resolution
      digitalWrite(MS2, LOW);
      digitalWrite(MS3, LOW);
    } break;
  }
}

void help()
{
  Serial.println("Montage specifications:");
  Serial.print("Each turn moves the platform by ");
  Serial.print(MM_BY_TURN);
  Serial.println(" mm.");
  Serial.print("There is ");
  Serial.print(STEP_BY_TURN);
  Serial.println(" steps by turn.");
  Serial.print("Each step moves the platform by ");
  Serial.print(MM_BY_TURN / (float)STEP_BY_TURN * 1000.0, 4);
  Serial.println(" um.");
  Serial.println();
  
  Serial.println("Stepper motor control commands:");
  Serial.println("{command_char}[[sign]{value}[unit]]{end_char}");
  Serial.println("[[sign]{value}[unit]] may be omitted if {command_char} do not need it.");
  Serial.println("[[sign]{value}[unit]] may be omitted if {command_char} is used as a getter-setter.");
  Serial.println("[sign] is optional.");
  Serial.print("[unit] is only used with the ");
  Serial.print(MOVE_CHAR);
  Serial.println(" {command_char}.");
  Serial.print("Buffer size is ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" character.");
  Serial.print(STEP_CHAR);
  Serial.println("\t: Steps the motor");
  Serial.print(TURN_CHAR);
  Serial.println("\t: Turns the lead screw");
  Serial.print(MOVE_CHAR);
  Serial.print("\t: Moves the platform in [unity]. May be ");
  Serial.print(CM_CHAR);
  Serial.print(", ");
  Serial.print(MM_CHAR);
  Serial.print(" or ");
  Serial.println(UM_CHAR);
  Serial.print(DELAY_CHAR);
  Serial.print("\t: Sets the delay in microsecond between each half step. Default is ");
  Serial.println(stepper_delay);
  Serial.print(FORWARD_CALIBRATION_CHAR);
  Serial.println("\t: Moves the platform to the front");
  Serial.print(BACKWARD_CALIBRATION_CHAR);
  Serial.println("\t: Moves the platform to the back");
  Serial.print(SOFT_STOP_CHAR);
  Serial.println("\t: Stops the current action");
  Serial.println("\\n\t: Ending character");
  Serial.println();
  
  Serial.print("Example: ");
  Serial.print(STEP_CHAR);
  Serial.println("400");
  Serial.println("Move forward 400 steps.");
  Serial.println();
  
  Serial.print("Example: ");
  Serial.print(MOVE_CHAR);
  Serial.print("-18.5");
  Serial.print(CM_CHAR);
  Serial.println("m");
  Serial.println("Move backward 18.5 cm.");
  Serial.println();
  
  Serial.print("Example: ");
  Serial.print(DELAY_CHAR);
  Serial.println("39");
  Serial.println("Set delay at 39 microsecond.");
  Serial.println();

  Serial.print("Example: ");
  Serial.println(DELAY_CHAR);
  Serial.println("Return delay value.");
  Serial.println();
}

