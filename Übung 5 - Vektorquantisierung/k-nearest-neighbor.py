# Autor: Julian Schlee 1821112
import numpy
import math
from PIL import Image


class Vector:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color  # 1==red ; -1==blue

    def __repr__(self):
        return "x: {x}, y: {y}, col: {c}".format(x=str(self.x), y=str(self.y), c=str(self.color))

    def get_distance(self, other_vector):
        return math.sqrt((other_vector.x - self.x)**2 + (other_vector.y - self.y)**2)


# Trainingsvektoren initialisieren
spiraldaten = open('spiral.txt', 'r')
lines = spiraldaten.readlines()
spiraldaten.close()

t_vektoren = []
for line in lines:
    pieces = line.split(";")
    t_vektoren.append(Vector(float(pieces[0]), float(pieces[1]), int(pieces[2])))


# KNN Algorithmus
K = 3  # Anzahl der Nachbarn
MAX = 1  # Länge der Achsen der Spiraldaten
MIN = -1  # Länge der Achsen der Spiraldaten
WIDTH = 500  # Breite der zu erstellenden Bilder
HEIGHT = 500  # Höhe der zu erstellenden Bilder
data_blue = numpy.zeros((WIDTH, HEIGHT, 3), dtype=numpy.uint8)  # Sammelt Pixel für die Erstellung der Bilder
data_red = numpy.zeros((WIDTH, HEIGHT, 3), dtype=numpy.uint8)  # "^
cur_x = 0  # Aktuelle x-Position bei Erstellung der Bilder
cur_y = 0  # Aktuelle y-Position bei Erstellung der Bilder
RED = [255, 0, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
for y in numpy.arange(MIN, MAX, 0.004000):  # -1.0000000 bis +1.0000000 in 0.004000er Schritten anstatt 0.000001er
    cur_x = 0                               # ^ dadurch => 2Mio * 2Mio px / 4000 => 500 * 500 px
    for x in numpy.arange(MIN, MAX, 0.004000):
        print("Currently working on pixel: " + str(cur_x) + "," + str(cur_y))
        tmp = Vector(x, y, 0)  # aktueller Eingabevektor

        # KNN finden
        min_values = [100000] * K
        min_indices = [0] * K
        for i in range(0, len(t_vektoren)):
            distance = tmp.get_distance(t_vektoren[i])
            for j in range(0, len(min_values)):
                if min_values[j] > distance:
                    min_values[j] = distance
                    min_indices[j] = i
                    break

        # Anhand der Farbe von KNN klassifizieren
        blue = 0
        red = 0
        for nn in range(0, K):
            if t_vektoren[min_indices[nn]].color == 1:
                red += 1
            else:
                blue += 1

        tmp.color = 1 if red > blue else -1

        # Pixel entsprechend der Klasse des Eingabevektors einfärben
        data_red[cur_x, cur_y] = WHITE if tmp.color == -1 else RED
        data_blue[cur_x, cur_y] = WHITE if tmp.color == 1 else BLUE

        cur_x += 1
    cur_y += 1


image_blue = Image.fromarray(data_blue)
image_red = Image.fromarray(data_red)

image_blue.save('blue.png')
image_red.save('red.png')
print("Process finished - images saved")
