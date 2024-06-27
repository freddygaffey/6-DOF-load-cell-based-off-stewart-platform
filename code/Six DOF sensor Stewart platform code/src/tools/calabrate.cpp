// #include <Arduino.h>
// #include "HX711.h"

// // take user input to set calibration factor for each load cell
// void setup() {
//     Serial.begin(9600);
//     Serial.println("Enter calibration factor for each load cell:");
//     str
    
// }
// }

#include <iostream>
using namespace std;

int main() {
  int x, y;
  int sum;
  cout << "Type a number: ";
  cin >> x;
  cout << "Type another number: ";
  cin >> y;
  sum = x + y;
  cout << "Sum is: " << sum;
  return 0;
}
