class comp():
    def __init__(self, asm):
        self.local_tree = asm

    def compair_neighbor_tree(self, tree: dict):
        # There are two main intuitive conditions for comparing the node tree of two sensors.
        # The first condition that has more priority; The condition is that the number of targets is less per sensor.
        # This condition gives priority to the decision that has more certainty.
        # The second condition is priority with the tree that contains the least number of nodes.
        # This main condition solves the defect of the first condition to some extent.
        # In the first condition, a sensor may make a decision that is more certain due to ignorance of the
        # overall topology, but the cause of certainty is ignorance.
        # The second condition prioritizes the sensors that have fewer neighbors. This condition
        # allows the sensor that has a  smaller range of awareness to make a decision to have a more preferable opinion.
        print(
            f"i am {self.name} and iam in comp , here my localtree "
            f": {self.local_tree}\n and here is received one : {tree}")

        my_tree_score = 0
        suggestion_tree_score = 0
        common_keys = set(self.local_tree.keys()) & set(tree.keys())
        for sensor in common_keys:
            if len(tree.get(sensor)) == len(self.local_tree.get(sensor)):
                continue
            elif len(tree.get(sensor)) == 1:
                suggestion_tree_score += 1
            elif len(self.local_tree.get(sensor)) == 1:
                my_tree_score += 1

        if my_tree_score == suggestion_tree_score:
            if len(list(self.local_tree.keys())) < len(list(tree.keys())):
                # I have better tree !
                return False
        if my_tree_score > suggestion_tree_score:
            # I have better tree
            return False

