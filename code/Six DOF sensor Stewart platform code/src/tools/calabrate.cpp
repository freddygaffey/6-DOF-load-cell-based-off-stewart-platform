#include <Arduino.h>
#include <HX711.h>

// Define the HX711 pins for each load cell individually
const int LOADCELL_DOUT_PINS[] = {2};  // Data output pin for load cell
const int LOADCELL_SCK_PINS[] = {12};  // Clock pin for load cell

HX711 scale;
float calibration_factor = 0.0;

void setup() {
    Serial.begin(230400); // Initialize serial communication at 230400 baud

    // Initialize the scale
    scale.begin(LOADCELL_DOUT_PINS[0], LOADCELL_SCK_PINS[0]);

    // Perform tare to reset the scale to zero
    Serial.println("Taring the scale...");
    scale.tare();

    Serial.println("Place a known weight on the scale...");
    delay(5000); // Wait for the user to place a known weight

    // Calibration: Read the weight value from the scale with a known weight
    float known_weight = 100.0; // Replace with your known weight in grams
    float raw_value = scale.get_units(10); // Get the average of 10 readings
    calibration_factor = raw_value / known_weight;
    scale.set_scale(calibration_factor);

    Serial.print("Calibration factor: ");
    Serial.println(calibration_factor);
}

void loop() {
    // Read and print the weight value
    float weight = scale.get_units(10); // Get the average of 10 readings
    Serial.print("Weight: ");
    Serial.print(weight);
    Serial.println(" grams");

    delay(1000); // Wait for 1 second before the next reading
}

