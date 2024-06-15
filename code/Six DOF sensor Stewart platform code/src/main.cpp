#include <Arduino.h>
#include "HX711.h"

// Define the HX711 pins for each load cell
const int LOADCELL_DOUT_PINS[6] = {32, 30, 28, 26, 24, 22};  // Data Out pins for each load cell
const int LOADCELL_SCK_PINS[6] = {33, 31, 29, 27, 25, 23};   // Clock pins for each load cell

HX711 scales[6];  // Array to hold HX711 objects for each load cell

// Define calibration factors for each load cell
float calibration_factors[6] = {0,0,0,0,0,0}; // Default values, adjust as necessary

void setup() {
  Serial.begin(230400); // Initialize serial communication at 1,000,000 baud

  // Initialize each HX711 module with the corresponding pins and calibration factor
  for (int i = 0; i < 6; i++) {
    scales[i].begin(LOADCELL_DOUT_PINS[i], LOADCELL_SCK_PINS[i]);
  }

  Serial.print("");
}

void loop() {
  // Print the weight in grams for each load cell
  for (int i = 0; i < 6; i++) {
    Serial.print(scales[i].get_units(), 1);
    if (i < 5) {
    Serial.print(",");
    }
  }

  Serial.println();
}
