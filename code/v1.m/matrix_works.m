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
b5 = [1 99 3];
b6 = [3 2 8];

f1 = analogRead(d15);
f2 = 2;
f3 = 2;
f4 = 42;
f5 = 76;
f6 = 675;



F = [f1 f2 f3 f4 f5 f6];

T = [
    i1,cross(b1,i1);
    i2,cross(b2,i2);
    i3,cross(b3,i3);
    i4,cross(b4,i4);
    i5,cross(b5,i5);
    i6,cross(b6,i6)];
    
result = F * T;
disp(result);



  






