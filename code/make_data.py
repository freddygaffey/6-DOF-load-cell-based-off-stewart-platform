import csv
import random
from os.path import join

how_much_data = int(input("how_much_data: "))

file = open("data.csv", "w")

for i in range(0, how_much_data):
    i = +1
    data = []
    for _ in range(6):
        insert = random.random()
        insert = str(insert * random.randrange(1, 1000))
        data.append(insert)
        if i % random.randint(1, 100) == 0:
            data = ["1", "sdfasd", "asdl", "2323"]
    file.write(",".join(data))
    file.write(
        """
    """
    )

file.close()
