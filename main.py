import pygame
from node import Node
from ant import Ant
import random
import time

pygame.init()
WIDTH = 700
HEIGHT = 700

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
    pathways = []
    phormone_decay = 500 # how many phormones are remembered delete everything else
    pathway_save_size = 300 # more will just slow it down
    phermones_strengh = 1 # how strong phormones counts are;        this is direct multiplication eg: 10*phermones_strengh
    while True:
        dtime = int(time.time() - dtime_start) # dtime count int
        clock.tick(99999) # set refresh rate unlimited = best
        display.fill([255,255,255]) # fill screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit("pygame.QUIT")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                nodes.append(Node(mousepos[0], mousepos[1]))
                phermones = []
                pathways = []
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ants.append(Ant(random.choice(nodes)))
                if event.key == pygame.K_q:
                    phermones = []
                    ants = []
                    pathways = []
                    nodes = []


        if len(phermones) > phormone_decay: # delete phermones that are old
            phermones = phermones[-phormone_decay:]
        for ant in ants:
            phermone = ant.move(nodes, phermones, phermones_strengh)     ####### DRIVER CODE #######
            phermones.append(phermone)
            if len(ant.visited_nodes) == len(nodes):
                pathways.append(ant.visited_nodes)

        if len(pathways) == pathway_save_size:
            pathways.remove(leastFrequent(pathways))
        if len(pathways) > pathway_save_size:
            pathways = []                                                       ### DISPLAY MAIN PATH ###
                                                                                # it shouldnt be the most frequent one you should check every node and see the most common pathway from that node
                                                                                # because current system is inefficient at displaying MAIN PATH for systems with many nodes
        #DRAW BEST CURRENT PATH
        if len(pathways) != 0:
            best_path = maxFreq(pathways)
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
        for phermone in phermones:
            pygame.draw.line(display, [1,1,1], phermone[0].pos, phermone[1].pos, 1)


        pygame.display.flip() # update


if __name__ == "__main__":
    main()