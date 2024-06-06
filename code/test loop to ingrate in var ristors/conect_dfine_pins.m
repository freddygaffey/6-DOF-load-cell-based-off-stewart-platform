% conect to boards
clear 
m = arduino('COM8','Mega2560');

F1V = readVoltage(m,"A7");
F2V = readVoltage(m,"A6");




FV = zeros(1,6);

log1 = 0;
log2 = 0;

for i = 1:1000
    % read volitige
    F1V = readVoltage(m,"A6");
    log1 = [log1,F1V];

uiy
    F1V = readVoltage(m,"A7");
    log2 = [log2,F2V];
    out = [log1',log2'];

    disp(F1V,F2V)

end 


out = [log1',log2']
plot(out,'DisplayName','out')