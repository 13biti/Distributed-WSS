class Sensor():
    def __init__(self, k: int, sensor_id: 2):
        self.local_tree = {2: ['t2'], 6: ['t2'], 1: ['t2']}
        self.neighbor = {3: ['t2', 't3', 't4'], 1: ['t2', 't3', 't1'], 6: ['t2', 't1']}
        # self.K = k
        self.target = ['t2', 't1']
        self.name = sensor_id
        # {target : [1 , 2] , }
        self.targetTracked = {}
        # {tracker_id : [target1 , ...]}
        self.node_tracking_status = {}
        self.assignment = {}
        self.K = k
        # self.recursive_backtracking(self.assignment)

    def node_status(self, node: int, list_of_target: list):
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
            if len(targetTracked.get(target)) < k:
                # if its can complit it self in future !
                if (k - len(targetTracked.get(target))) <= self.candidates_to_track(target, assignment,
                                                                                    targetTracked):
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
        if len(list(self.assignment.keys())) == len(list(self.node_tracking_status.keys())):
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

