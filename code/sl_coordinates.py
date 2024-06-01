import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from services.general import dump_orjson
# Coordinates of the polygon
polygon_coords = [
    (3499.77, 1500.07),
    (5798.43, 3799.93),
    (6452.11, 3150.56),
    (5401.44, 2099.71),
    (5751.91, 1749.63),
    (4500.10, 498.92),
]

# Create a polygon from the coordinates
polygon = Polygon(polygon_coords)

# Function to generate hexagonal grid points
def hexagonal_grid(polygon, radius):
    min_x, min_y, max_x, max_y = polygon.bounds
    dx = 3/2 * radius
    dy = np.sqrt(3) * radius

    x_coords = np.arange(min_x - radius, max_x + dx, dx)
    y_coords = np.arange(min_y - radius, max_y + dy, dy)
    hex_points = []
    
    for i, x in enumerate(x_coords):
        for j, y in enumerate(y_coords):
            if i % 2 == 0:
                py = y
            else:
                py = y + dy / 2
            point = Point(x, py)
            if polygon.intersects(point.buffer(radius)):
                hex_points.append(point)
    
    return hex_points

# Generate hexagonal grid points within the polygon
hex_radius = 30  # Radius of hexagonal circles
sniffer_points = hexagonal_grid(polygon, hex_radius)

# Extract x and y coordinates of the sniffer points
x_coords = [point.x for point in sniffer_points]
y_coords = [point.y for point in sniffer_points]

# Plot the polygon and the sniffer points
x_poly, y_poly = polygon.exterior.xy
# plt.figure(figsize=(10, 10))
# # plt.plot(x_poly, y_poly, 'b-', label='Polygon')
# # plt.scatter(x_coords, y_coords, c='r', label='Sniffer Locations')
# plt.plot(x_poly, y_poly, 'b-')
# plt.scatter(x_coords, y_coords, color="red", alpha=0.5)
# plt.axis('off')
# plt.gca().set_aspect('equal', adjustable='box')
# plt.legend()
# plt.savefig('monaco.png', transparent=True)
# # plt.xlabel('X Coordinate')
# # plt.ylabel('Y Coordinate')
# # plt.title('Hexagonal Grid of Sniffer Locations')
# plt.show()

# Print the selected sniffer locations
selected_locations = [[point.x, point.y] for point in sniffer_points]
print(len(selected_locations))
print("Selected sniffer locations (x, y):")
print(selected_locations)
# for loc in selected_locations:
#     print(loc)

dump_orjson('new_sniffer_location.json', {"sniffer_location": selected_locations})
    