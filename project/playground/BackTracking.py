class BackTracking:
    def __init__(self, k):
        # {target : [1 , 2] , }
        self.targetTracked = {}
        # {tracker_id : [target1 , ...]}
        self.node_tracking_status = {}
        self.assignment = {}
        self.K = k
        # self.recursive_backtracking(self.assignment)

    def update_node_status(self, node: int, list_of_target: list):
        # print(f"46 some one want to update me like that {node} , {list_of_target} og state : {self.node_tracking_status}")
        self.node_tracking_status[node] = list_of_target

        # if its new target in system , it should added to list so we know about it !!
        # this for just want to add new target to list !
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

    # this method is checking if this specific target can get enough sensor in future or not !
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
            if target in list(targetTracked.keys()):
                if len(targetTracked.get(target)) < k:
                    if (k - len(targetTracked.get(target))) <= self.candidates_to_track(target, assignment, targetTracked):
                            domain_list.append(target)

        domain_list.sort(reverse=True, key=lambda item: len(self.targetTracked.get(item, [])))
        return domain_list

    def reset_backtracking(self):
        for target in list(self.targetTracked.keys()):
            self.targetTracked[target] = []

    #this method can call in 2 ways , if you have target_tracker list , send it and itw work , if not
    # it will use it own list , this is good when i dont want to use its default constractor value , but
    # this is poor implimentation , so
    # when use it , you can create 2 instance and use them as you wish !
    def recursive_backtracking(self, assignment, target_tracker):
        if len(target_tracker) == 0:
            target_tracker = self.targetTracked

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
                        target_tracker.setdefault(value, []).append(Node)
                        # self.update_target_tracker(value , Node)
                        # self.targetTracked.setdefault(value, []).append(Node)
                        result = self.recursive_backtracking(assignment, target_tracker)
                        if result:
                            return result
                        assignment[Node].remove(value)
            return False
