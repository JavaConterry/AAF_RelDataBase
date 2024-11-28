class BTreeNode:
    def __init__(self, degree, is_leaf=True):
        self.degree = degree
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def is_full(self):
        return len(self.keys) == 2 * self.degree - 1


class BTreeIndex:
    def __init__(self, degree=2):
        self.root = BTreeNode(degree)
        self.degree = degree

    def total_data_length(self):
        return self._calculate_total_data_length(self.root)

    def _calculate_total_data_length(self, node):
        total_length = sum(len(data_list) for _, data_list in node.keys)
        if not node.is_leaf:
            for child in node.children:
                total_length += self._calculate_total_data_length(child)
        return total_length

    def search(self, key, operator="="):
        results = []
        if operator == "=":
            self._search_exact(self.root, key, results)
        elif operator == "<":
            self._search_less_than(self.root, key, results)
        elif operator == ">":
            self._search_greater_than(self.root, key, results)
        return results

    def _search_exact(self, node, key, results):
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1

        if i < len(node.keys) and node.keys[i][0] == key:
            results.extend(node.keys[i][1])

        if not node.is_leaf:
            self._search_exact(node.children[i], key, results)

    def _search_less_than(self, node, key, results):
        i = 0
        while i < len(node.keys) and node.keys[i][0] < key:
            results.extend(node.keys[i][1])
            i += 1
        if not node.is_leaf:
            for j in range(i + 1):
                self._search_less_than(node.children[j], key, results)

    def _search_greater_than(self, node, key, results):
        i = 0
        while i < len(node.keys):
            if node.keys[i][0] > key:
                results.extend(node.keys[i][1])
                if not node.is_leaf:
                    self._search_greater_than(node.children[i], key, results)
            i += 1

        if not node.is_leaf:
            self._search_greater_than(node.children[-1], key, results)

    def insert(self, key, data):
        root = self.root
        if root.is_full():
            new_root = BTreeNode(self.degree, is_leaf=False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, data)

    def _insert_non_full(self, node, key, data):
        if node.is_leaf:
            for i, (k, v) in enumerate(node.keys):
                if k == key:
                    node.keys[i][1].append(data)
                    return

            node.keys.append((key, [data]))
            node.keys.sort(key=lambda x: x[0])
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1

            if node.children[i].is_full():
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1

            self._insert_non_full(node.children[i], key, data)

    def split_child(self, parent, index):
        degree = self.degree
        full_child = parent.children[index]
        new_child = BTreeNode(degree, is_leaf=full_child.is_leaf)

        parent.keys.insert(index, full_child.keys[degree - 1])
        parent.children.insert(index + 1, new_child)

        new_child.keys = full_child.keys[degree:(2 * degree - 1)]
        full_child.keys = full_child.keys[0:(degree - 1)]

        if not full_child.is_leaf:
            new_child.children = full_child.children[degree:(2 * degree)]
            full_child.children = full_child.children[0:degree]