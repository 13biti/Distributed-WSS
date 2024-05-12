class Sensor():

    def __init__(self, k: int, sensor_id: 2):
        self.local_tree = {2: ['t2'], 6: ['t2'], 3: ['t2'], 1: ['X']}
        self.neighbor = {3: ['t2', 't3', 't4'], 1: ['t2', 't3', 't1'], 6: ['t2', 't1']}
        # self.K = k
        self.target = ['t2', 't1']
        self.name = sensor_id
        # self.messenger = MessageManager()

        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
    def compair_neighbor_tree(self, tree: dict):
        if len(list(self.local_tree.keys())) < len(list(tree.keys())):
            return False
        # if len of my tree is bigger , so i am lose !
        elif len(list(self.local_tree.keys())) > len(list(tree.keys())):
            for node in list(tree.keys()):
                self.node_status(node, tree.get(node))
            self.reset_backtracking()
            self.update_local_tree()
            return True
        # now lets take care of equality , this is the hard part , in this section , i will create new tree base on
        # sujested information , then i will compair thouse two tree ,
        elif len(list(self.local_tree.keys())) == len(list(tree.keys())):
            psudo_assignment = {}
            psudo_targetTracked = {}
            common_Node = set(self.local_tree.keys()) & set(tree.keys())
            for node in list(self.local_tree.keys()):
                psudo_assignment.setdefault(node, [])
                if node in common_Node:
                    psudo_assignment[node].append(tree.get(node))
            for target in self.target:
                psudo_targetTracked.setdefault(target, [])
                for node in list(tree.keys()):
                    if target in tree.values(node):
                        psudo_targetTracked[target].append(node)
            psudo_tree, psudo_targetTracked = self.recursive_backtracking(psudo_assignment, psudo_targetTracked)
            if self.is_haveBetter_tree(self.local_tree, psudo_tree):
                print("its better !")
            else:
                print("hory fuck it ! ")


    def is_haveBetter_tree(self, local_tree, psudo_tree):
        friendly_score = {}
        local_tree_score = 0
        psudo_tree_score = 0
        for node in list(self.neighbor.keys()):
            social_score = len(self.neighbor.get(node))
            friendly_score.setdefault(node, social_score)
        for node in list(self.local_tree.keys()):
            if local_tree.get(node) == "X" and psudo_tree.get(node) != []:
                if friendly_score.get(node) == 1:
                    local_tree_score -= 1
                    psudo_tree_score += 1
                else:
                    local_tree_score += friendly_score.get(node)
            elif local_tree.get(node) != "X" and psudo_tree.get(node) == []:
                if friendly_score.get(node) == 1:
                    local_tree_score += 1
                    psudo_tree_score -= 1
                else:
                    psudo_tree_score += friendly_score.get(node)
            else:
                pass
        if local_tree_score > psudo_tree_score :
            return False
        else:
            return True

inst = Sensor(3,2)
inst.compair_neighbor_tree( {2: ['X'], 1: ['X'], 4: ['X'], 5: ['X'], 3: ['X']})

