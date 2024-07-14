import numpy as np

calculation_required = float(input("i = 0 or b = 1: "))

# insert 2 points X Y Z 
if calculation_required == 0:
    print("insert 2 points X Y Z you are calculating i")
    try:
        x1 = float(input("X1: "))
        y1 = float(input("Y1: "))
        z1 = float(input("Z1: "))

        x2 = float(input("X2: "))
        y2 = float(input("Y2: "))
        z2 = float(input("Z2: "))

        a = np.array([x1, y1, z1])
        b = np.array([x2, y2, z2])

        ab = np.subtract(b, a)

        abm = np.sqrt(ab[0]**2 + ab[1]**2 + ab[2]**2)
        ab = ab/abm

        print(f"ab: {ab[0]}, {ab[1]}, {ab[2]}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
if calculation_required == 1:
    print("insert 1 point X Y Z you are calculating b")
    x1 = float(input("X1: "))
    y1 = float(input("Y1: "))
    z1 = float(input("Z1: "))

    b = np.array([x1, y1, z1])
    print(f"b: {b[0]}, {b[1]}, {b[2]}")
