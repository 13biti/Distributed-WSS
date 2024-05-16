class Sensor():
    def __init__(self, k: int, sensor_id: 2):
        self.local_tree = {}
        self.neighbor = {3: ['t2', 't3', 't4'], 1: ['t2', 't3', 't1'], 6: ['t2', 't1']}
        # self.K = k
        self.target = ['t2', 't1']
        self.name = sensor_id
        # {target : [1 , 2] , }
        self.targetTracked = {}
        # {tracker_id : [target1 , ...]}
        self.node_tracking_status = {2: ['t2', 't1'], 3: ['t2', 't3', 't4'], 1: ['t2', 't3', 't1'], 6: ['t2', 't1']}
        self.assignment = {}
        self.K = k
        # self.recursive_backtracking(self.assignment)


    def update_node_status(self, node: int, list_of_target: list):
        print(
            f"46 some one want to update me like that {node} , {list_of_target} og state : {self.node_tracking_status}")
        self.node_tracking_status[node] = list_of_target
        # for target in list(self.target_can_tracked_by_node.values())[0]:
        #     print(target)
        #     if target not in targets:
        #         targets.append(target)
        #         self.update_target_tracker(target)
        for item in list_of_target:
            if item not in list(self.targetTracked.keys()):
                self.update_target_tracker(item)

    def update_target_tracker(self, target, tracker=None):
        if tracker is None:
            self.targetTracked.setdefault(target, [])
            return
        self.targetTracked[target].append(tracker)

    def unassigned_Node(self, assignment, targetTracked):
        unassigned_Node_list = []
        for element in self.node_tracking_status.keys():
            if element not in list(targetTracked.values()) and element not in list(assignment.keys()):
                unassigned_Node_list.append(element)

        unassigned_Node_list.sort(reverse=False, key=lambda item: len(
            [tar for tar in self.node_tracking_status.get(item, []) if
             tar not in [useless for useless in self.targetTracked.keys() if
                         len(targetTracked.get(useless, [])) == self.K]]))
        # unassigned_Node_list.sort(reverse=False, key=lambda item: len(self.domain_values2(item, self.K)))
        #  len([tar for tar in self.target_can_tracked_by_node.get(item, []) if tar not in assignment.get(item, [])]))
        return unassigned_Node_list

    def eligible_to_conditions(self, target, tracker, k):
        # First, check that the desired target has tracker comparison :: it checked in domain
        # > also , The condition of communication must also be established :: it always true !
        # if len(self.targetTracker.get(target)) < k  and \
        #     (k - len(self.targetTracker.get(target))) <= self.candidates_to_track(target) and \
        #     tracker not in self.targetTracker.get(target):
        if target != "":
            return True

    def candidates_to_track(self, target, assignment, target_tracked):
        var = self.unassigned_Node(assignment, target_tracked)
        counter = 0
        for element in var:
            if target in self.node_tracking_status.get(element):
                counter += 1
        return counter

    def domain_values(self, tracker, k, targetTracked, assignment):
        # try to ordred based on  need to tracker , in god mod , one get all other nothing !
        # > also should check if other can tolk with this tracker or not !
        domain_list = []
        for target in self.node_tracking_status.get(tracker):
            if target in list(targetTracked.keys()) :
                if len(targetTracked.get(target)) < k:
                    # if its can complit it self in future !
                    if (k - len(targetTracked.get(target))) <= self.candidates_to_track(target, assignment, targetTracked):
                        if tracker not in targetTracked.get(target):
                            domain_list.append(target)

        if len(domain_list) != 0:
            print("final domain back ", domain_list)
            # return domain_list

        domain_list.sort(reverse=True, key=lambda item: len(self.targetTracked.get(item, [])))
        return domain_list

    def reset_backtracking(self):
        for target in list(self.targetTracked.keys()):
            self.targetTracked[target] = []


    def recursive_backtracking(self, assignment, target_tracker):
        if len(list(assignment.keys())) == len(list(self.node_tracking_status.keys())):
            return assignment, target_tracker
        for Node in self.unassigned_Node(assignment, target_tracker):
            domain = self.domain_values(Node, self.K, target_tracker, assignment)
            if len(domain) == 0:
                assignment.setdefault(Node, [])
                return self.recursive_backtracking(assignment, target_tracker)
            else:
                for value in domain:
                    if self.eligible_to_conditions(value, Node, self.K):
                        assignment.setdefault(Node, []).append(value)
                        if value is None:
                            target_tracker.setdefault(Node, [])
                        else:
                            target_tracker[value].append(Node)
                        # self.update_target_tracker(value , Node)
                        # self.targetTracked.setdefault(value, []).append(Node)
                        result = self.recursive_backtracking(assignment, target_tracker)
                        if result:
                            return result
                        assignment[Node].remove(value)
            return False

    def compair_neighbor_tree(self, tree: dict):
        # in this new compair fucntion , first i want to check if the sujjested tree is smaller of not , if it is , i will prifer it , if not
        # i will check them in my new is_better function , which will check the both tree base on creating new tree with sujested one ,
        # the tree which that free frindlear nood , will win , i will complite this note
        # ------------------------------------------------------
        # my tree is better !
        # print("iam in comp ! ------------------------------")
        # if len(list(self.local_tree.keys())) < len(list(tree.keys())):
        #     return False
        # # if len of my tree is bigger , so i am lose !
        # elif len(list(self.local_tree.keys())) > len(list(tree.keys())):
        #     for node in list(tree.keys()):
        #         self.update_node_status(node, tree.get(node))
        #     self.reset_backtracking()
        #     self.update_local_tree()
        #     return True
        # # now lets take care of equality , this is the hard part , in this section , i will create new tree base on
        # # sujested information , then i will compair thouse two tree ,
        # elif len(list(self.local_tree.keys())) == len(list(tree.keys())):
        psudo_target_tracked = {}
        psudo_assignment = {}
        common_Node = set(self.local_tree.keys()) & set(tree.keys())
        for node in list(self.local_tree.keys()):
            psudo_assignment.setdefault(node, [])
            if node in common_Node:
                psudo_assignment[node] = tree.get(node)
        for target in self.target:
            psudo_target_tracked.setdefault(target, [])
            for node in list(tree.keys()):
                if target in tree.get(node):
                    psudo_target_tracked[target].append(node)
        print(
            f"98iam {self.name} recive tree from {-1} lets got to isbe ! with psudos : {psudo_assignment} and {psudo_target_tracked} and here recived tree {tree}")
        psudo_tree, psudo_target_tracked = self.recursive_backtracking(psudo_assignment, psudo_target_tracked)
        print(
            f"99iam {self.name} recive tree from {-1} lets got to isbe ! with psudos : {psudo_tree} and {psudo_target_tracked} and here is my tree {self.local_tree} ")
        if self.is_haveBetter_tree(self.local_tree, psudo_tree):
            print(f"78 soemthing is better iam {self.name} between {self.local_tree} and {psudo_tree} ")
            for node in list(psudo_tree.keys()):
                if psudo_tree.get(node) == 'X':
                    self.update_node_status(node, [])
                    psudo_assignment.setdefault(node, self.neighbor.get(node))
                else:
                    print(
                        f"43 going to update node status like this in ct {node, psudo_tree} more info : {self.name, tree}")
                    self.update_node_status(node, psudo_tree.get(node))
                    psudo_assignment.setdefault(node, psudo_tree.get(node))
            self.reset_backtracking()
            self.local_tree = psudo_assignment
            return True
        else:
            return False

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
        if local_tree_score > psudo_tree_score:
            return False
        else:
            return True
    def update_local_tree(self, assignment=None):
        # this function only get called when something get chaange in neighbor status !
        # so i have neighbor status , i will use it to create tree , after that i will compair that tree with og one ,
        # if its better then we have new tree ,
        print(f"00 {self.name} i want to update!")
        psudo_target_tracked = {}
        psudo_assignment = {}
        # for node in list(self.neighbor.keys()):
        #     psudo_assignment.setdefault(node, [])
        # psudo_assignment.setdefault(self.name , [])

        for target in self.target:
            psudo_target_tracked.setdefault(target, [])
        print(f"00 {self.name}i want to back with {psudo_assignment} , {psudo_target_tracked} and {self.node_tracking_status}")
        result = self.recursive_backtracking(psudo_assignment, psudo_target_tracked)
        if result :
            psudo_tree, psudo_target_tracked = result
        else:
            return False
        # now we have new tree , which is can be  better or not , so lets comp!
        print(f"00 {self.name} i want to comp with {psudo_tree} , {self.local_tree}")
        if self.is_haveBetter_tree(self.local_tree, psudo_tree):
            for node in list(psudo_tree.keys()):
                if not psudo_tree.get(node):
                    self.update_node_status(node, [])
                    psudo_assignment[node] = ["X"]
                else:
                    # print(f"43 going to update node status like this in ct {node,  psudo_tree} more info ")
                    self.update_node_status(node, psudo_tree.get(node))
                    psudo_assignment[node] = psudo_tree.get(node)
            self.assignment = psudo_tree
            self.local_tree = psudo_tree
            return True
        return False


inst = Sensor(3, 2)
inst.update_local_tree()
inst.compair_neighbor_tree({2: [], 1: [], 4: [], 5: [], 3: []})


