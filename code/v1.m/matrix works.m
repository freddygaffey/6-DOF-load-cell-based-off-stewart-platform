
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

F = [1 2 3 4 5 6];

T = [
    i1,cross(b1,i1);
    i2,cross(b2,i2);
    i3,cross(b3,i3);
    i4,cross(b4,i4);
    i5,cross(b5,i5);
    i6,cross(b6,i6)];
    
result = F * T;
disp(result);



  






