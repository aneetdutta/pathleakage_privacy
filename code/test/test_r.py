class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0

# Given dictionary
data = {
    "W1": ["L1", "L1`", "L1``"],
    "L1": ["W1", "W1`"],
    "L1`": ["W1"],
    "W2": ["L2"],
    "L1``": ["W1", "W1`"]
}

# Initialize UnionFind
uf = UnionFind()

# Add all elements to UnionFind and union them based on mappings
for key, mappings in data.items():
    uf.add(key)
    for item in mappings:
        uf.add(item)
        uf.union(key, item)

# Create a dictionary to store the components
components = {}

# Find the root for each item and group them
for item in uf.parent:
    root = uf.find(item)
    if root not in components:
        components[root] = []
    components[root].append(item)

# Get the final list of merged components
result = list(components.values())

print(result)
