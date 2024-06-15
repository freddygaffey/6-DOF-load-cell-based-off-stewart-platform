// #include <Arduino.h>
// #include "HX711.h"

// // Define the HX711 pins for each load cell
// const int LOADCELL_DOUT_PINS[6] = {32, 30, 28, 26, 24, 22};  // Data Out pins for each load cell
// const int LOADCELL_SCK_PINS[6] = {35, 33, 31, 29, 27, 23};   // Clock pins for each load cell

// HX711 scales[6];  // Array to hold HX711 objects for each load cell

// void setup() {
//   Serial.begin(250000); // Initialize serial communication at 1,000,000 baud

//   Serial.println("HX711 Demo");
//   Serial.println("Testing load cells individually");

//   // Initialize each HX711 module with the corresponding pins
//   for (int i = 0; i < 100000; i++) {
//     scales[i].begin(LOADCELL_DOUT_PINS[i], LOADCELL_SCK_PINS[i]);
//     Serial.print("Testing load cell ");
//     Serial.print(i + 1);
//     Serial.print(":");
//     Serial.print(" Read: \t\t");
//     Serial.println(scales[i].read());

//     // Tare the scale to set the current load to 0
//     scales[i].tare();

//     Serial.print("After taring load cell ");
//     Serial.print(i + 1);
//     Serial.print(":");
//     Serial.print(" Read: \t\t");
//     Serial.println(scales[i].read());
//   }

//   Serial.println("Load cell testing complete.");
// }

// void loop() {
//   // This function is empty for now, but you can add any additional code you need
// }