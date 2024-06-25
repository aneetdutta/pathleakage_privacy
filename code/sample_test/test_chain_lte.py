class UnionFind:
    def __init__(self):
        self.parent = {}
    
    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]
    
    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        if root1 != root2:
            self.parent[root2] = root1
    
    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item

def group_identifiers(tuples_list):
    uf = UnionFind()
    
    for _, _, identifiers in tuples_list:
        identifiers = list(identifiers)
        for identifier in identifiers:
            uf.add(identifier)
        for i in range(1, len(identifiers)):
            uf.union(identifiers[0], identifiers[i])
    
    groups = {}
    for identifier in uf.parent:
        root = uf.find(identifier)
        if root not in groups:
            groups[root] = set()
        groups[root].add(identifier)
    
    return list(groups.values())

# Example input
tuples_list = [
    (1, 'A', {'RNTI_70'}),
    (6, 'L', {'RNTI_71'}),
    (6, 'L', {'RNTI_71', 'RNTI_70'}),
    (6, 'L', {'RNTI_71'}),
    (6, 'L', {'RNTI_72'}),
    (6, 'L', {'RNTI_71', 'RNTI_72'}),
    (2, 'G', {'RNTI_73'}),
    (3, 'C', {'RNTI_74', 'RANDOM_345ae04768'}),
]

# Grouping the tuples
grouped_identifiers = group_identifiers(tuples_list)
print(grouped_identifiers)
