#include <Arduino.h>

#include <NewPing.h>
#include "FSME.h"
#define MAX_DISTANCE 100 // Maximum distance (in cm) to ping.
#define DELAY 20
//#define DEBUG
#define INFRARED
//#define ULTRASOUND

#ifdef INFRARED
  #define LEFT_PIN A0
  #define RIGHT_PIN A1
  #define IR_THRESHOLD 300
#endif

#ifdef ULTRASOUND
  #define THRESHOLD 70
  #define SONAR_NUM 2      // Number of sensors.

  NewPing sonar[SONAR_NUM] = {   // Sensor object array.
    NewPing(4, 5, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping. 
    NewPing(6, 7, MAX_DISTANCE)
  };
#endif

uint16_t left_d, right_d;

int32_t counter = 0;

// 
uint8_t readSensors();
void printSensors();
uint8_t sensorsState = 0;
//


// for the FSM
enum STATE
{
  idle,
  left_first,
  right_first,
  person_in,
  person_out
};

FSME fsm;
State states[5];
// transiciones
Transition * idle_trans[2];
Transition * left_first_trans[2];
Transition * right_first_trans[2];
Transition * person_in_trans[1];
Transition * person_out_trans[1];

// for timeouts
uint32_t actualTime(void) {
  return millis();
}


// prototypes for state actions
void idle_action();
void left_first_action();
void right_first_action();
void person_in_action();
void person_out_action();
// prototypes for events
uint8_t noObstacle();
uint8_t leftObstacle();
uint8_t rightObstacle();
uint8_t bothObstacle();

void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  // FSM init

  // fsm transitions
  idle_trans[0] = new EvnTransition(leftObstacle, left_first);
  idle_trans[1] = new EvnTransition(rightObstacle, right_first);

  //left_first_trans[0] = new EvnTransition(noObstacle, idle);
  left_first_trans[0] = new EvnTransition(rightObstacle, person_in);
  left_first_trans[1] = new TimeTransition(2000, idle);

  //right_first_trans[0] = new EvnTransition(noObstacle, idle);
  right_first_trans[0] = new EvnTransition(leftObstacle, person_out);
  right_first_trans[1] = new TimeTransition(2000, idle);

  person_in_trans[0] = new TimeTransition(5, idle);
  person_out_trans[0] = new TimeTransition(5, idle);
  
  // fsm states and actions
  states[idle].setState(idle_action, idle_trans, 2);
  states[left_first].setState(left_first_action, left_first_trans, 2);
  states[right_first].setState(right_first_action, right_first_trans, 2);
  states[person_in].setState(person_in_action, person_in_trans, 1);
  states[person_out].setState(person_out_action, person_out_trans, 1);

  fsm.setStates(states, 5);
  fsm.setInitialState(idle);

}

void loop() { 
  
  sensorsState = readSensors(); 
  //printSensors();
  fsm.run();
}

void printSensors()
{
  Serial.print(left_d);
  Serial.print("-");
  Serial.println(right_d);
}

uint8_t readSensors()
{
  #ifdef ULTRASOUND
    delay(40);
    left_d = sonar[0].ping_cm(MAX_DISTANCE);
    left_d = left_d < THRESHOLD && left_d != 0;
    
    delay(40);
    right_d = sonar[1].ping_cm(MAX_DISTANCE);
    right_d = right_d < THRESHOLD && right_d != 0; 
  #endif
  delay(DELAY);
  left_d = analogRead(LEFT_PIN) > IR_THRESHOLD;
  delay(DELAY);
  right_d = analogRead(RIGHT_PIN) > IR_THRESHOLD;
  
  return (left_d << 1) | (right_d);
}

/// FSM events
uint8_t noObstacle()
{
  return left_d == 0 && right_d == 0;
}
uint8_t leftObstacle()
{
  return left_d && right_d == 0;
}
uint8_t rightObstacle()
{
  return right_d && left_d == 0;
}
uint8_t bothObstacle()
{
  return left_d && right_d;
}

/// FSM actions
void idle_action()
{
  if(fsm.isStateChanged())
  {
    // entry action
    #ifdef DEBUG
      printSensors();
      Serial.println("entering idle.");
    #endif
  }
}
void left_first_action()
{
  if(fsm.isStateChanged())
  {
    // entry action
    #ifdef DEBUG
    printSensors();
    Serial.println("entering left_first.");
    #endif
  }
}
void right_first_action()
{
  if(fsm.isStateChanged())
  {
    // entry action
    #ifdef DEBUG
    printSensors();
    Serial.println("entering right_first.");
    #endif
  }
}
void person_in_action()
{
  if(fsm.isStateChanged())
  {
    // entry action
    counter++;
    #ifdef DEBUG
    printSensors();
    Serial.print("entering person_in. Count: ");
    Serial.println(counter);
    #endif
    Serial.println("I");
  }
}
void person_out_action()
{
  if(fsm.isStateChanged())
  {
    // entry action
    counter--;
    #ifdef DEBUG
    printSensors();
    Serial.print("entering person_out. Count: ");
    Serial.println(counter);
    #endif
    Serial.println("O");
  }
}
