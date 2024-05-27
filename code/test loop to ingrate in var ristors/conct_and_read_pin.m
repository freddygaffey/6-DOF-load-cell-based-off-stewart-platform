clc
clear a 
a = arduino('COM6','ESP32-WROOM-DevKitC');
a.AvailableAnalogPins;

configurePin(a,"D2","AnalogInput")
configurePin(a,"D4","AnalogInput")
configurePin(a,"D12","AnalogInput")
configurePin(a,"D13","AnalogInput")
configurePin(a,"D14","AnalogInput")
configurePin(a,"D15","AnalogInput")



F1V = readVoltage(a,"D2");
F2V = readVoltage(a,"D4");
F3V = readVoltage(a,"D12");
F4V = readVoltage(a,"D13");
F5V = readVoltage(a,"D14");
F6V = readVoltage(a,"D15");

