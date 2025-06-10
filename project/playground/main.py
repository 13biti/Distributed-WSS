from typing import Dict
from BackTracking import BackTracking
import json
import socket
import socket
import multiprocessing
import time

import jsonSenderAndReceiver

from enum import Enum


class Status(Enum):
    UNCHANGED = 1
    CHANGED = 2


# lets see how backtraking will work :
# first


class Sensor(BackTracking):
    def __init__(self, neighbor: list, k: int, sensor_id: int):
        super().__init__(k)
        self.local_tree = {}
        # will be something like {neighborId : [list of target]}
        self.neighbor: Dict[int, list[str]] = {}
        # self.K = k
        self.target = []
        self.suggestion_list = {}
        self.name = sensor_id

        self.targetState = Status.UNCHANGED
        self.treeState = Status.UNCHANGED
        # self.messenger = MessageManager()

        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
        for element in neighbor:
            self.neighbor[element] = []

    def sensor(self, sencedObj: list):
        sensor_port = self.name + 19000
        self.sense_object(sencedObj)
        # self.update_local_tree()

        # start receiving message
        messenger = jsonSenderAndReceiver.MessageManager(sensor_port)
        messenger.start_receiving()

        # asking  neighbor to send message :
        # all of this methids are jsut run for once , thy like constractore for this class
        # i should seprate them !
        for neg in list(self.neighbor.keys()):
            self.update_node_status(neg, [])
            # sending message  like : message , host , port
            # for now all sensore have same host which is local host !
            messenger.sending_message({0: [[], {}]}, socket.gethostname(), 19000 + neg)
        # it may update with empty list in future , case we dont know about targets , but for now , i assume i have them right now
        # overall this will work with once time updating the list , for more updates on targets  , for that i shuld run it like cron job or something !
        self.update_node_status(self.name, self.target)
        # end of constractore !

        have_change = (
            self.treeState == Status.CHANGED or self.targetState == Status.CHANGED
        )
        while True:
            # print(f"A1 {self.name} say here the general buffer:", messenger.general_buffer, "have change ? ", have_change)
            # print(f"A2 {self.name} say my backresult is : {self.local_tree} come from {self.neighbor}")

            # send statues(localtree and target) to neighbor !
            if have_change:
                for neg in list(self.neighbor.keys()):
                    if neg != self.name:
                        print(
                            f"{self.name} send to---> {neg} =>  ",
                            {self.name: [self.target, self.local_tree]},
                        )
                        messenger.sending_message(
                            {self.name: [self.target, self.local_tree]},
                            socket.gethostname(),
                            19000 + neg,
                        )
                have_change = False
            # if len(list(messenger.general_buffer.keys())) != 0:
            #     have_c
            if len(list(messenger.general_buffer.keys())) > 0:
                for _ in list(messenger.general_buffer.keys()):
                    # get one message ::
                    # message will be something look like this : {name : [targets , tree]}
                    tmp = messenger.get_buffer()
                    print(f"A6 recive somehting this is how message loook like ! {tmp}")

                    negstate = self.update_neighbor_status(tmp[0], tmp[1][0])
                    print(
                        f"A6 + {self.name} here is my neighbor_status after update : {self.neighbor} , {negstate}"
                    )
                    if negstate:
                        self.reset_backtracking()
                        self.update_local_tree()
                    localChanges = True if self.treeState == Status.CHANGED else False
                    print(
                        f"A--- + {self.name} here is my tree! after update : {self.local_tree} + {self.neighbor} + {self.target}"
                    )
                    print(
                        f"A8 iam {self.name} recive tree from {tmp[0]} lets got to comp ! with {tmp[1][1]} and here is my tree {self.local_tree}nag {self.neighbor} , targ {self.target}"
                    )
                    print(f"A* i am {self.name} here is change status {self.treeState}")
                    treeState = self.compair_neighbor_tree(tmp[1][1])
                    neigborCahngeMe = treeState
                    if not neigborCahngeMe and localChanges:
                        have_change = True

                print(self.local_tree)
            # print(self.local_tree)
            # ther is no comp for now !
            #
            # f"A8 iam {self.name} recive tree from {tmp[0]} lets got to comp ! with {tmp[1][1]} and here is my tree {self.local_tree}nag {self.neighbor} , targ {self.target}")
            # if tmp[1][1] != {}:
            #     treeState = self.compair_neighbor_tree(tmp[1][1])
            #     if treeState:
            #         have_change = True

            # print(self.local_tree)

    def sense_object(self, targets: list):
        # it needs to change to 2 dimension
        # update target list
        if set(self.target) != set(targets):
            self.target = targets
            self.targetState = Status.CHANGED

    def update_neighbor_status(self, neighborId: int, neighborTargetList: list):
        # neighborStatus is something look like this :
        # { neighbor_id : [ target 1 , target 2 , ... .. .  ] }
        # its important to not update neigbor status with old state of other negbor , but still should
        # update if its validate data ,thats what update_node_status is doing !
        # its only get neighbor status from neighbor it self
        if neighborId in list(self.neighbor.keys()):
            if self.neighbor.get(neighborId) == neighborTargetList:
                return False
            else:
                self.neighbor[neighborId] = neighborTargetList
                self.update_node_status(neighborId, neighborTargetList)
                # self.update_node_status(self.name, self.target)
                self.assignment.setdefault(neighborId, [])
                return True

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
            for sen in list(self.neighbor.keys()):
                if (
                    len(self.neighbor.get(sen, [])) == 1
                    and self.neighbor.get(sen, [])[0] == self.target[0]
                ):
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.values())[0]
                    if counter == self.K - 1:
                        print(self.suggestion_list)
                        return True
        # are sensor have multiple target
        # It is very important that we do our best at this stage to involve K 'single target' node
        # I want to use backtracking !

        for element in self.target:
            self.suggestion_list[self.name] = self.target
            for sen in list(self.neighbor.keys()):
                if sen not in list(
                    self.suggestion_list.keys()
                ) and element in self.neighbor.get(sen):
                    print(self.neighbor.get(sen))
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.get(sen, []))
                    if counter == self.K - 1:
                        print(self.suggestion_list)
                        return True
        if counter != self.K - 1:
            print("target cannot get tracked")
            return False

    def update_node_tracking_status(self):
        node_tracking_status = {}
        for node in self.neighbor:
            node_tracking_status.setdefault(node, self.neighbor.get(node))
            node_tracking_status.setdefault(self.name, self.target)
        return node_tracking_status

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
        #
        # for target in self.target:
        #     psudo_target_tracked.setdefault(target, [])
        # this code is just for now , in future you should change it ! , first create instawnce of backtracking , then ,
        # insert them in there not in here !!
        self.node_tracking_status = self.update_node_tracking_status()

        print(
            f"00 {self.name}i want to back with {psudo_assignment},{psudo_target_tracked} and {self.node_tracking_status}"
        )
        result = self.recursive_backtracking(psudo_assignment, psudo_target_tracked)
        if result:
            print(f"A01 holy crap {self.name} , here is result funck it {result}")
            psudo_tree, psudo_target_tracked = result
        else:
            return False
        # now we have new tree , which is can be  better or not , so lets comp!
        print(f"A00 {self.name} i want to comp with {psudo_tree} , {self.local_tree}")
        if self.is_haveBetter_tree(self.local_tree, psudo_tree):
            print(
                f"A01 , holy fuck , i am {self.name} psudo is fucking accepted , here it is : {psudo_tree}"
            )
            for node in list(psudo_tree.keys()):
                if not psudo_tree.get(node):
                    self.update_node_status(node, [])
                    psudo_assignment[node] = ["X"]
                else:
                    # print(f"43 going to update node status like this in ct {node,  psudo_tree} more info ")
                    self.update_node_status(node, psudo_tree.get(node))
                    psudo_assignment[node] = psudo_tree.get(node)
            # print(f"45.5 here is what i {self.name} want to set on localtree {psudo_tree} , here is ass { psudo_assignment} and fuck it  ")
            self.local_tree = psudo_assignment
            self.treeState = Status.CHANGED
            return True
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
        if tree == {}:
            return False

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
            f"98iam {self.name} recive tree from {-1} lets got to isbe ! with psudos : {psudo_assignment} and {psudo_target_tracked} and here recived tree {tree}"
        )
        result = self.recursive_backtracking(psudo_assignment, psudo_target_tracked)
        if result:
            psudo_tree, psudo_target_tracked = result
        else:
            psudo_tree, psudo_target_tracked = {}, {}
        print(
            f"99iam {self.name} recive tree from {-1} lets got to isbe ! with psudos : {psudo_tree} and {psudo_target_tracked} and here is my tree {self.local_tree} "
        )
        if self.is_haveBetter_tree(self.local_tree, psudo_tree):
            print(
                f"78 soemthing is better iam {self.name} between {self.local_tree} and {psudo_tree} "
            )
            for node in list(psudo_tree.keys()):
                if not psudo_tree.get(node):
                    self.update_node_status(node, ["X"])
                    psudo_assignment.setdefault(node, ["X"])
                else:
                    print(
                        f"43 going to update node status like this in ct {node, psudo_tree} more info : {self.name, tree}"
                    )
                    self.update_node_status(node, psudo_tree.get(node, []))
                    psudo_assignment.setdefault(node, psudo_tree.get(node))
            self.reset_backtracking()
            self.local_tree = psudo_assignment
            self.treeState = Status.CHANGED
            return True
        else:
            return False

    def is_haveBetter_tree(self, local_tree, psudo_tree):
        print(
            f"---! in better  lc :{local_tree} , pt : {psudo_tree} more info : {self.name} , neighbor : {self.neighbor}"
        )
        friendly_score: Dict[int, int] = {}
        local_tree_score = 0
        psudo_tree_score = 0
        for node in list(self.neighbor.keys()):
            social_score = len(self.neighbor.get(node, []))
            friendly_score.setdefault(node, social_score)
        social_score = len(self.target)
        friendly_score.setdefault(self.name, social_score)
        for node in list(self.local_tree.keys()):
            if local_tree.get(node) == ["X"] and psudo_tree.get(node) != []:
                if friendly_score.get(node) == 1:
                    psudo_tree_score += 1
                else:
                    local_tree_score += friendly_score.get(node, 0)
            elif local_tree.get(node) != ["X"] and psudo_tree.get(node) == []:
                if friendly_score.get(node) == 1:
                    local_tree_score += 1
                    psudo_tree_score -= 1
                else:
                    psudo_tree_score += friendly_score.get(node, 0)
            else:
                pass
        if local_tree_score > psudo_tree_score:
            return False
        else:
            return True

        # one of this two will happen ! node is lonly and can track only one tartget , wich mean
        # now i should create new tree !


if __name__ == "__main__":
    # ins1 = Sensor([2 ,3], 2, 1)
    # process1 = multiprocessing.Process(target=ins1.sensor, args=(["t2", "t3", "t1"], ))
    # process1.start()
    # ins2 = Sensor([1,3], 2, 2)
    # process2 = multiprocessing.Process(target=ins2.sensor, args=(["t2", "t3", "t1"],))
    # process2.start()
    # ins3 = Sensor([1 ,2], 2, 3)
    # process3 = multiprocessing.Process(target=ins3.sensor, args=(["t2", "t3", "t1"],))
    # process3.start()
    # ins1 = Sensor([2, 3], 2, 1)
    # process1 = multiprocessing.Process(target=ins1.sensor, args=(["t2", "t3", "t1"],))
    #
    # ins2 = Sensor([1, 3], 2, 2)
    # process2 = multiprocessing.Process(target=ins2.sensor, args=(["t2", "t1", "t3"],))
    #
    # ins3 = Sensor([2, 1], 2, 3)
    # process3 = multiprocessing.Process(target=ins3.sensor, args=(["t2", "t3", "t4"],))

    # ins4 = Sensor([5, 3, 1], 3, 4)
    # process4 = multiprocessing.Process(target=ins4.sensor, args=(["t3", "t4"],))
    #
    # ins5 = Sensor([3, 4], 3, 5)
    # process5 = multiprocessing.Process(target=ins5.sensor, args=(["t3", "t4"],))
    #
    # ins6 = Sensor([1, 2], 3, 6)
    # process6 = multiprocessing.Process(target=ins6.sensor, args=(["t2", "t1"],))
    #
    # process6.start()
    # process5.start()
    # # process4.start()
    # process2.start()
    # process1.start()
    # process1.start()
    # #
    # ins1 = Sensor([3, 2, 6, 4], 3, 1)
    # ins1.sensor(["t2", "t3", "t1"])
    #
    # ins2 = Sensor([1,3,6], 3, 2)
    # ins2.sensor(["t2", "t1", "t3 "])
    #
    # ins3 = Sensor([2, 1, 4, 5], 3, 3)
    # ins3.sensor(["t2", "t3", "t4"])
    #
    # ins4 = Sensor([5, 3, 1], 3, 4)
    # ins4.sensor(["t3", "t4"])
    #
    # ins5 = Sensor([3, 4], 3, 5)
    # ins5.sensor(["t3", "t4"])
    #
    # ins6 = Sensor([1, 2], 3, 6)
    # ins6.sensor(["t2", "t1"])
    #
    # make instance like this : list_of_neighbor + how_many_sensore_need_to_track + sensor_id )
    # then add them to process so they work simultansly , in the code ,they will talk using spcefic port
    # in sensore method , thy will sence the thing !
    ins1 = Sensor(neighbor=[2], k=2, sensor_id=1)
    process1 = multiprocessing.Process(target=ins1.sensor, args=(["t2", "t3", "t1"],))

    ins2 = Sensor(neighbor=[1], k=2, sensor_id=2)
    process2 = multiprocessing.Process(target=ins2.sensor, args=(["t2", "t1"],))

    #    ins3 = Sensor([2, 1, 4, 5], 3, 3)
    #    process3 = multiprocessing.Process(target=ins3.sensor, args=(["t2", "t3", "t4"],))
    #
    #    ins4 = Sensor([5, 3, 1], 3, 4)
    #    process4 = multiprocessing.Process(target=ins4.sensor, args=(["t3", "t4"],))
    #
    #    ins5 = Sensor([3, 4], 3, 5)
    #    process5 = multiprocessing.Process(target=ins5.sensor, args=(["t3", "t4"],))
    #
    #    ins6 = Sensor([1, 2], 3, 6)
    #    process6 = multiprocessing.Process(target=ins6.sensor, args=(["t2", "t1"],))
    #
    #    process6.start()
    #    process5.start()
    #    process4.start()
    #    process3.start()
    process2.start()
    process1.start()


# ins1.compair_neighbor_tree({1: ['t2'], 2: ['t2'], 6: ['t2'], 3: ["t2", "t4", "t3"]})
