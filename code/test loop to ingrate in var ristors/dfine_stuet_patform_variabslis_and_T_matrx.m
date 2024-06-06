% to cnect to esp throgh COM6 to pins D2,D4,D12-D15

% look at paper
i1 = [1 2 3];
i2 = [3 2 1];
i3 = [1 2 3];
i4 = [3 2 1];
i5 = [1 42 3];
i6 = [3 2 1];

b1 = [1 2 3];
b2 = [3 2 1];
b3 = [1 2 3];
b4 = [3 2 1];
b5 = [1 9 3];
b6 = [3 2 8];


% Force = [F1V,F2V,F3V,F4V,F5V,F6V];

T = [
    i1,cross(b1,i1);
    i2,cross(b2,i2);
    i3,cross(b3,i3);
    i4,cross(b4,i4);
    i5,cross(b5,i5);
    i6,cross(b6,i6)];
    

result = Force * T;   


outputresult = result;
inputForces = rand(1,6);

for i = 1:10
    Force = Force;
T = [
    i1,cross(b1,i1);
    i2,cross(b2,i2);
    i3,cross(b3,i3);
    i4,cross(b4,i4);
    i5,cross(b5,i5);
    i6,cross(b6,i6)];

result = Force* T;
outputresult = [outputresult;result];
inputForces = [inputForces;Force]; 
end


O = zeros(i+1,1);
finalOutput = [inputForces,O,outputresult]
 






