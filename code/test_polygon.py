from shapely.geometry import Point, Polygon
from services.general import extract_orjson
# Define the polygon vertices
polygon_coords = [
    (3499.77, 1500.07),
    (5798.43, 3799.93),
    (6799.91, 2799.96),
    (4500.10, 498.92)
]

polygon_coords = [
    (3499.77,1500.07),
    (5798.43,3799.93),
    (6452.11,3150.56),
    (5401.44,2099.71),
    (5751.91,1749.63),
    (4500.10,498.92),
]

# Create a polygon object
polygon = Polygon(polygon_coords)

# Function to check if a point is inside the polygon
def is_point_inside_polygon(x, y, polygon):
    point = Point(x, y)
    return polygon.contains(point)

# Example points
points = [
    (4000, 2000),
    (7000, 3000),
    (6501.76,2742.54),
    (4591.31,780.42),
    (5650.46,1275.92),
    (6552.12,2687.73),
    [4096.5997513129405, 918.000709032878]
]

# points = extract_orjson("new_sniffer_location.json")["sniffer_location"]
# Check each point
for x, y in points:
    if is_point_inside_polygon(x, y, polygon):
        print(f"Point ({x}, {y}) is inside the polygon.")
    else:
        print(f"Point ({x}, {y}) is outside the polygon.")