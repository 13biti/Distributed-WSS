from typing import Dict


class BackTracking:
    def __init__(self):
        # target : [1 , 2]
        self.targetTracker ={}
        # tracker_id : [target1 , ...]
        self.target_can_tracked_by_node = {}
        self.assignment = {}
        # self.recursive_backtracking(self.assignment)

    def node_status(self, node: int, list_of_target: list):
        self.target_can_tracked_by_node[node] = list_of_target
        # for target in list(self.target_can_tracked_by_node.values())[0]:
        #     print(target)
        #     if target not in targets:
        #         targets.append(target)
        #         self.update_target_tracker(target)
        for item in list_of_target:
            if item not in list(self.targetTracker.keys()):
                self.update_target_tracker(item)

    def update_target_tracker(self, target, tracker=None):
        if tracker is None:
            self.targetTracker.setdefault(target, [])
            return
        self.targetTracker[target].append(tracker)

    def unassigned_variable(self):
        unassigned_variable_list = []
        for element in self.target_can_tracked_by_node.keys():
            if element not in list(self.targetTracker.values()):
                unassigned_variable_list.append(element)
        return unassigned_variable_list

    def eligible_to_conditions(self, target, tracker, k):
        # First, check that the desired target has tracker comparison
        # > also , The condition of communication must also be established
        # if len(self.targetTracker.get(target)) < k  and \
        #     (k - len(self.targetTracker.get(target))) <= self.candidates_to_track(target) and \
        #     tracker not in self.targetTracker.get(target):
        if target != "":
            return True

    def candidates_to_track(self, target):
        var = self.unassigned_variable()
        counter = 0
        for element in var:
            if target in self.target_can_tracked_by_node.get(element):
                counter += 1
        return counter

    def domain_values(self, tracker, k):
        # try to ordred by need to tracker , in god mod , one get all outher nothing !
        # > also should check if other can tolk with this tracker or not !
        domain_list = []
        for target in self.target_can_tracked_by_node.get(tracker):
            #print(self.targetTracker.get(target))
            if len(self.targetTracker.get(target)) < k :
                if (k - len(self.targetTracker.get(target))) <= self.candidates_to_track(target):
                    domain_list.append(target)

        if domain_list is not None:
            domain_list.sort(reverse=False, key=lambda item: len(self.targetTracker.get(item, [])))
            print(domain_list)
            return domain_list

        return [""]
    def recursive_backtracking(self, assignment):
        if len(list(self.assignment.keys())) == len(list(self.target_can_tracked_by_node.keys())):
            return assignment
        variable = self.unassigned_variable();
        for item in variable:
            #print(self.domain_values(item, 3))
            for value in self.domain_values(item, 3):
                if self.eligible_to_conditions(value, item, 3):
                    self.assignment.setdefault(item, []).append(value)
                    result = self.recursive_backtracking(assignment)
                    if result != False:
                        return result
                    assignment[item].remove(value)
        return False
        # var = ( lambda item : item not in self.unassigned_variable())


class Sensor(BackTracking):

    def __init__(self, neighbor: list, k: int, sensor_id: int):
        super().__init__()
        self.neighbor = {}
        self.K = k
        self.target = []
        self.suggestion_list = {}
        self.name = sensor_id

        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
        for element in neighbor:
            self.neighbor[element] = []

    def sense_object(self, target):
        # it needs to change to 2 dimension
        # update target list
        for element in self.target:
            if element not in target:
                self.target.remove(element)

        for element in target:
            if element not in self.target:
                self.target.append(element)

    def update_neighbor_status(self, neighbor_status: Dict[int, list]):
        # neighborStatus is something look like this :
        # { neighbor_id : [ target 1 , target 2 , ... .. .  ] }
        # print(list(neighbor_status.keys())[0])
        self.neighbor[list(neighbor_status.keys())[0]] = list(neighbor_status.values())[0]

    def create_local_tree(self):
        # Different situations of problem :
        # A :
        # If the sensor has only one target in its list,
        # it looks for K neighbors in the list that has similar conditions
        # and offers cooperation to the other sensor(s).

        # B :
        # If the sensor had one target and no similar neighbors (one target);
        # Suggests to K random neighbor, but it only changes its array
        #    (maybe a better decision will be made in the future for other sensor)

        # C :
        # If it has one target and a neighbor does not know the target, or if it has more than one target
        # it waits for a message from other neighbors for a proposal
        # (the final tree will be formed in nodes with several targets.
        #   The wait continues until the neighbors of a target make a decision.
        #   their decision will reduce the decision range of other neighbors!
        #   In the best case, a sequential decision will be made, but in normal conditions,
        #   if it still has uncertain conditions, it will try to make a decision using tree with the largest number of target
        #   Backtracking algorithm will be the main solution in this situation .)
        counter = 0
        if len(self.target) == 1:
            self.suggestion_list[self.name] = self.target
            for sen in (list(self.neighbor.keys())):
                if len(self.neighbor.get(sen)) == 1 and self.neighbor.get(sen)[0] == self.target[0]:
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.values())[0]
                    if counter == self.K - 1:
                        print(self.suggestion_list)
                        return
        # are sensor have multiple target
        # It is very important that we do our best at this stage to involve K 'single target' node
        # I want to use backtracking !

        for element in self.target:
            self.suggestion_list[self.name] = self.target
            for sen in (list(self.neighbor.keys())):
                if sen not in list(self.suggestion_list.keys()) and element in self.neighbor.get(sen):
                    print(self.neighbor.get(sen))
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.get(sen))
                    if counter == self.K - 1:
                        print(self.suggestion_list)
                        return

        if counter != self.K - 1:
            print("target cannot get tracked")

    def update_local_tree(self):
        self.node_status(self.name, self.target)
        for node in list(self.neighbor.keys()):
            self.node_status(node, self.neighbor.get(node))
        result = self.recursive_backtracking(self.assignment)
        print(result)
    # def sort_unassigned_variable_list(unassigned_variable_list ):


if __name__ == '__main__':
    ins1 = Sensor([2, 3, 4, 5], 3, 1)
    ins1.sense_object(["t1"])
    ins1.update_neighbor_status({2: ["t1", "t2", "t3"]})
    ins1.update_neighbor_status({3: ["t1"]})
    ins1.update_neighbor_status({4: ["t1"]})
    ins1.update_neighbor_status({5: ["t1"]})
    ins1.create_local_tree()
    ins1.update_local_tree()
