import pygame
from node import Node
from ant import Ant
import random
import time
import math

pygame.init()
WIDTH = 700
HEIGHT = 700

def measurePathLength(path): # this will find the length of path from node to node
    lenght = 0
    for index, _ in enumerate(path):
        lenght += math.hypot(path[index-1].pos[0]-path[index].pos[0],path[index-1].pos[1]-path[index].pos[1])
    return lenght

def leastFrequent(arr):
    count = arr.count(maxFreq(arr)) # very inefficient but will work
    selection = maxFreq(arr)        #            --||--
    for item in arr:
        if arr.count(item) < count:
            count = arr.count(item)
            selection = item
         
    return selection
    
def maxFreq(arr):
    count = 0
    selection = 0
    for item in arr:
        if arr.count(item) > count:
            count = arr.count(item)
            selection = item
         
    return selection
 
def main():
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    dtime_start = time.time()
    nodes = []
    ants = []
    phermones = []
    best_path = []
    current_best_path_length = 100000000000000000 # just big
    phormone_decay = 1000 # how many phormones are remembered delete everything else
    phermones_strengh = 1 # how strong phormones counts are;        this is direct multiplication eg: 10*phermones_strengh
    while True:
        dtime = int(time.time() - dtime_start) # dtime count int
        clock.tick(999999) # set refresh rate unlimited = best
        display.fill([255,255,255]) # fill screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit("pygame.QUIT")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                nodes.append(Node(mousepos[0], mousepos[1]))
                phermones = []
                best_path = []
                current_best_path_length = 10000000
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ants.append(Ant(random.choice(nodes)))
                if event.key == pygame.K_q:
                    phermones = []
                    ants = []
                    nodes = []
                    best_path = []
                    current_best_path_length = 100000000000000000 # just big


        if len(phermones) > phormone_decay: # delete phermones that are old
            phermones = phermones[-phormone_decay:]
        for ant in ants:
            phermone = ant.move(nodes, phermones, phermones_strengh)     ####### DRIVER CODE #######
            phermones.append(phermone)
            if len(ant.visited_nodes) == len(nodes):
                len_path = measurePathLength(ant.visited_nodes)
                if len_path < current_best_path_length:
                    current_best_path_length = len_path
                    best_path = ant.visited_nodes

        #DRAW BEST CURRENT PATH
        for i, line in enumerate(best_path):
            pygame.draw.line(display, [0,255,150], line.pos, best_path[i-1].pos, 5)


        #DRAW NODES
        for node in nodes:
            pygame.draw.circle(display, [0,0,0], node.pos, 6,6)
        

        #DRAW ANTS # will be flickering
        for ant in ants:
            pygame.draw.circle(display, [255,0,0], ant.current_node.pos, 10,10)
            for unavailable_move in ant.visited_nodes:
                pygame.draw.circle(display, [0,255,0], unavailable_move.pos, 5,5)


        #DRAW PHERMONES
        #for phermone in phermones:
        #    pygame.draw.line(display, [1,1,1], phermone[0].pos, phermone[1].pos, 1)


        pygame.display.flip() # update


if __name__ == "__main__":
    main()