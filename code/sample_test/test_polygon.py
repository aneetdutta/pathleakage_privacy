from shapely.geometry import Point, Polygon
# Define the polygon vertices
# polygon_coords = [
#     (3499.77, 1500.07),
#     (5798.43, 3799.93),
#     (6799.91, 2799.96),
#     (4500.10, 498.92)
# ]

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
    (4408.45,2262.60),
    (4573.07,1705.79),
    (5989.28,3308.41),
    (5952.97,3625.55)
]

# points = extract_orjson("new_sniffer_location.json")["sniffer_location"]
# Check each point
for x, y in points:
    if is_point_inside_polygon(x, y, polygon):
        print(f"Point ({x}, {y}) is inside the polygon.")
    else:
        print(f"Point ({x}, {y}) is outside the polygon.")