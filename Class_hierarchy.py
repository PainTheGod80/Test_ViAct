class ClassHierarchyParser:
    def __init__(self, hierarchy_file, id_to_name_file):
        self.hierarchy_file = hierarchy_file
        self.id_to_name_file = id_to_name_file
        self.class_hierarchy = {}
        self.name_to_id = {}

    def parse_files(self):
        with open(self.hierarchy_file, 'r') as hierarchy_file:
            for line in hierarchy_file:
                parent, child = line.strip().split()
                self.class_hierarchy[child] = parent

        with open(self.id_to_name_file, 'r') as id_to_name_file:
            for line in id_to_name_file:
                parts = line.strip().split('\t')
                category_id = parts[0]
                class_names = parts[1]
                for class_name in str(class_names).split(','):
                    self.name_to_id[class_name] = category_id

    def find_siblings(self, class_name):
        parent = self.class_hierarchy.get(class_name)
        if parent is None:
            return []
        siblings = []
        for child, parent_class in self.class_hierarchy.items():
            if parent_class == parent and child != class_name:
                siblings.append(child)
        return siblings

    def find_parent(self, class_name):
        return self.class_hierarchy.get(class_name)

    def find_ancestors(self, class_name):
        ancestors = []
        current_class = class_name
        while current_class in self.class_hierarchy:
            parent = self.class_hierarchy[current_class]
            ancestors.append(parent)
            current_class = parent
        return ancestors

    def have_common_ancestor(self, class1, class2):
        ancestors1 = set(self.find_ancestors(class1))
        ancestors2 = set(self.find_ancestors(class2))
        return bool(ancestors1.intersection(ancestors2))


def main():
    parser = ClassHierarchyParser('technical_test_2023_07/question3/hierarchy.txt', 'technical_test_2023_07/question3/id_to_name.txt')
    parser.parse_files()

    class1 = 'n05760202'
    class2 = 'n02430045'

    siblings = parser.find_siblings(class1)
    print(f"Siblings of {class1}: {siblings}")

    parent = parser.find_parent(class1)
    print(f"Parent of {class1}: {parent}")

    ancestors = parser.find_ancestors(class1)
    print(f"Ancestors of {class1}: {ancestors}")

    has_common_ancestor = parser.have_common_ancestor(class1, class2)
    print(f"Common ancestor between {class1} and {class2}: {has_common_ancestor}")

if __name__ == '__main__':
    main()
