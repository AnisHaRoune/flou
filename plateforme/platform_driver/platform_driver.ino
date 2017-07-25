#include "motor_control.h"

void setup()
{
  pinMode(DEBUG_LED, OUTPUT);
  motorControlSetup();
  Serial.begin(9600);
  Serial.println("Begin platform driver");
}

char input_buffer[BUFFER_SIZE];

void loop()
{
  read_buffer(input_buffer, BUFFER_SIZE);

  digitalWrite(DEBUG_LED, HIGH);
  digitalWrite(EN, LOW); //Pull enable pin low to set FETs active and allow motor control

  char command = input_buffer[0];
  switch (command)
  {
    case STEP_CHAR:
    {
      int32_t steps = String(&input_buffer[1]).toInt();
      step_stepper(steps);
    } break;
    case TURN_CHAR:
    {
      float turns = String(&input_buffer[1]).toFloat();
      int32_t steps = turns * STEP_BY_TURN;
      Serial.print((float)steps / STEP_BY_TURN, 7);
      Serial.print(" turn ");
      step_stepper(steps);
    } break;
    case MOVE_CHAR:
    {
      move_platform(input_buffer, BUFFER_SIZE);
    } break;
    case FORWARD_CALIBRATION_CHAR:
    {
      Serial.print("FORWARD_CALIBRATION");
      calibration(FORWARD);
    } break;
    case BACKWARD_CALIBRATION_CHAR:
    {
      Serial.print("BACKWARD_CALIBRATION");
      calibration(BACKWARD);
    } break;
    case DELAY_CHAR:
    {
      unsigned int s = String(&input_buffer[1]).toInt();
      if (s > 0)
      {
        set_speed(s);
      }
      Serial.println(get_speed());
    } break;
    case HELP_CHAR:
    {
      help();
    } break;
    default:
    {
      invalid_syntax();
    } break;
  }

  digitalWrite(EN, HIGH); //Pull enable pin high to set FETs active and stop motor control and noises
  digitalWrite(DEBUG_LED, LOW);
}

void move_platform(char input_buffer[], size_t buffer_size)
{
  float value = String(&input_buffer[1]).toFloat();
      
  int i;
  for (i = 0; (i < buffer_size) && (input_buffer[i] != END_CHAR); i++); //Find last char
  char unit[2] = { input_buffer[i - 2], input_buffer[i - 1] }; //Get unit chars
  if (unit[1] == 'm')
  {
    switch (unit[0])
    {
      case CM_CHAR:
      {
        int32_t steps = value * 10 / MM_BY_TURN * STEP_BY_TURN;
        Serial.print((float)steps / 10 * MM_BY_TURN / STEP_BY_TURN, 7);
        Serial.print(" cm ");
        step_stepper(steps);
      } return;
      case MM_CHAR:
      {
        int32_t steps = value / MM_BY_TURN * STEP_BY_TURN;
        Serial.print((float)steps * MM_BY_TURN / STEP_BY_TURN, 7);
        Serial.print(" mm ");
        step_stepper(steps);
      } return;
      case UM_CHAR:
      {
        int32_t steps = value / MM_BY_TURN * STEP_BY_TURN / 1000;
        Serial.print((float)steps * MM_BY_TURN / STEP_BY_TURN * 1000, 7);
        Serial.print(" um ");
        step_stepper(steps);
      } return;
    }
  }

  invalid_syntax();
}

void invalid_syntax()
{
  Serial.println("Invalid syntax, press h for help.");
}

void read_buffer(char input_buffer[], size_t buffer_size)
{
  clean_up_buffers(input_buffer, BUFFER_SIZE);
  
  size_t input_size = 0;
  char input = 0;
  while((input_size < buffer_size) && (input != END_CHAR))
  {
    if (Serial.available())
    {
      input = Serial.read();
      input_buffer[input_size++] = input;
    }
  }
}

void clean_up_buffers(char input_buffer[], size_t buffer_size)
{
  for (int i = 0; i < buffer_size; i++)
  {
    input_buffer[i] = '\0';
  }
  
  Serial.flush();
  while (Serial.available())
  {
    Serial.read();
  }
}
