//Programa para testear el envío de datos a un servo mediante arduino.
// Permite verificar que funciona el servo.

#include <Servo.h>

#define NUM_SERVOS 2

Servo servos[NUM_SERVOS];  // Array with 2 servos
int servoPins[NUM_SERVOS] = {5,6};  // Pines PWM pins where servos are connected (link 1 -> 5, link 2 -> 6)


int pos = 0;    // posicion del servo

void setup() {
  Serial.begin(9600);   // Comunicación serie a 9600 baudios

  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(servoPins[i]);  // Asocia cada servo a su pin
  }
}

void loop() {

  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read until line break
    int sep = data.indexOf(',');                 // Look for the comma

    if (sep > 0) {
      int servoNum = data.substring(0, sep).toInt();
      int jointValue = data.substring(sep + 1).toInt();
      servos[servoNum-1].write(jointValue);
    }
  }
}
