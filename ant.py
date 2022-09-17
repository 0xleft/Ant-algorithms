import random
from math import hypot
import numpy as np


class Ant():
    def __init__(self, starting_node):
        self.current_node = starting_node
        self.prev_move = starting_node
        self.visited_nodes = [starting_node]
        print(f'new ant at {self.current_node.pos}')

    def move(self, nodes, phermones, phermones_strengh):
        weights, nodes_local = self.findWeights(nodes, phermones, phermones_strengh)
        to_node = self.chooseMove(nodes_local, weights)
        self.prev_move = self.current_node
        self.current_node = to_node # to_node has to an object
        self.visited_nodes.append(self.current_node)
        return (self.prev_move, to_node) # phermones


    def chooseMove(self, nodes, weights):
        choice = random.choices(nodes, weights, k=1) # returns a list
        return choice[0]
    
    def findWeights(self, nodes, phermones, phermones_strengh):
        
        nodes_local = nodes[:] # local deep copy of nodes
        for visited_node in self.visited_nodes:
            nodes_local.remove(visited_node)
        
        if len(nodes_local) == 0:
            nodes_local = nodes[:] # deep copy of nodes
            self.visited_nodes = [self.current_node]
            nodes_local.remove(self.current_node) # we dont want to go where we are curenly

        phermones_counts = [(phermones.count((self.current_node, node))+phermones.count((node, self.current_node))) for node in nodes_local]
        distances_clean = [list(np.subtract(self.current_node.pos, node.pos)) for node in nodes_local]
        distances = [hypot(distance[0], distance[1]) for distance in distances_clean]
        
        distances_phermones = [float(weight+phermones_counts[i]*phermones_strengh) for i,weight in enumerate(distances)]
        max_distance = max(distances_phermones)+1 # add one so one even the highest value has a chance at being selected

        weights_distances = [abs((max_distance-distance)/max_distance) for distance in distances_phermones]

        sum_of_weights_not_full = np.sum(weights_distances)
        weights_full = [weight/sum_of_weights_not_full for weight in weights_distances]


        return weights_full, nodes_local
