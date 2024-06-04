import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.patches import RegularPolygon

# Define the size of the square grid
grid_size = 10

# Calculate the size of the square
square_size = 1000  # assuming a square of 1000x1000 units

# Radius of circles
radius = 30
hex_height = radius * np.sqrt(3)
hex_width = 2 * radius
horiz_spacing = hex_width * 3/4
vert_spacing = hex_height

# Generate points in a square grid
x_range = np.linspace(0, square_size, grid_size)
y_range = np.linspace(0, square_size, grid_size)
circle_centers = []
hex_centers = []

for i, x in enumerate(x_range):
    for j, y in enumerate(y_range):
        # Offset every other row by half the width of a circle
        if i % 2 == 0:
            circle_center = (x, y)
        else:
            circle_center = (x, y + vert_spacing / 2)
        circle_centers.append(circle_center)
        
        # Calculate hexagon centers
        hex_centers.append((x + hex_width / 2, y + hex_height / 2))
        
# Number of shapes required
num_shapes = len(circle_centers)

# Plotting the result
fig, ax = plt.subplots()
ax.set_aspect('equal')

# Draw the square
square_coords = [(0, 0), (square_size, 0), (square_size, square_size), (0, square_size)]
poly_patch = Polygon(square_coords, closed=True, fill=None, edgecolor='r')
ax.add_patch(poly_patch)

# Draw the circles
for center in circle_centers:
    circle_patch = Circle(center, radius, fill=None, edgecolor='b', linestyle='--')
    ax.add_patch(circle_patch)

# Draw the hexagons
for center in hex_centers:
    hexagon = RegularPolygon(center, numVertices=6, radius=radius, orientation=np.radians(30), fill=None, edgecolor='g', linestyle='-')
    ax.add_patch(hexagon)

plt.xlim(-50, square_size + 50)
plt.ylim(-50, square_size + 50)
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.savefig('square_with_overlapping_shapes.png', transparent=True, dpi=600)
