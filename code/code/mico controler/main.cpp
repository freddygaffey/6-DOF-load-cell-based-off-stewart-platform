//on luinx (it works for manjaro) you need to run $ sudo chmod 666 ..//..//../../../dev/ttyUSB0 

#include <Arduino.h>
#include "HX711.h" //https://github.com/RobTillaart/HX711 "I think"

// Define the HX711 pins for each load cell
const int LOADCELL_DOUT_PINS[] = {32, 33, 25, 26, 27, 14};  
const int LOADCELL_SCK_PINS[] = {19, 18, 5, 17, 16, 4};

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




