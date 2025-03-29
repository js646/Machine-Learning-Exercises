from PIL import Image
import numpy

RED = [255, 0, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]

data = numpy.zeros((120, 120, 3), dtype=numpy.uint8)
for i in range(0, 120):
    for j in range(0, 120):
        data[i, j] = RED if i < 60 else WHITE

print("finished")
image = Image.fromarray(data)
image.save('test.png')
