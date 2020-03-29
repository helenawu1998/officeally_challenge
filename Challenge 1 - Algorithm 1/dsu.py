class DSU:
    """Disjoint-set data structure for maintaining sets of patient records.
    """
    def __init__(self, n):
        self.fa = [x for x in range(n)]

    def find(self, x):
        if x == self.fa[x]:
            return x
        self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def union(self, x, y):
        a = self.find(x)
        b = self.find(y)
        self.fa[b] = a