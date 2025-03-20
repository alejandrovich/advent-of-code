

class Solution:
    # define node class
    # - cost
    # - path
    
    def __init__(self):
        # read the input
        # set up coordinate space
        # set up obstacle positions (1024)
        # initialize variables:
        # - starting position
        # - ending position
        # - visited nodes hash
        # - unvisited nodes (ordered by cost)

    def recurse(self):
        # visit the least expensive node
        # if it is end: return
        # else:
        # - get its unseen neighbors
        #  - compute neighbor cost (current cost + 1)
        #  - compute path to reach
        # - save unseen to unvisited DS

        node = self.get_shortest()
        while node and not self.is_end(node):
            neighbors = self.get_neighbors(node)
            for n in neighbors:
                self.save_unvisited(n)






