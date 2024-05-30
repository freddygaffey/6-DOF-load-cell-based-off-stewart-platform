% conect to boards
clear a 
clear m
a = arduino('COM6','ESP32-WROOM-DevKitC');
m = arduino('COM8','Mega2560');


a.AvailableAnalogPins;

% configer pins
configurePin(a,"D2","AnalogInput")
configurePin(a,"D4","AnalogInput")
configurePin(a,"D12","AnalogInput")
configurePin(a,"D13","AnalogInput")
configurePin(a,"D14","AnalogInput")
configurePin(a,"D15","AnalogInput")
   

FV = zeros(1,6);



for i = 1:10
    % read volitige
    F1V = readVoltage(a,"D2");
    F2V = readVoltage(a,"D4");
    F3V = readVoltage(a,"D12");
    F4V = readVoltage(a,"D13");
    F5V = readVoltage(a,"D14");
    F6V = readVoltage(a,"D15");


    %dislay and log
    FVoutput = [F1V,F2V,F3V,F4V,F5V,F6V];
    FVlog = [FVlog;FVoutput];
    disp(FVoutput)
end 




