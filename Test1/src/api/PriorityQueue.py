import heapq

class PriorityQueue:
    def __init__(self):
        self.ele = []
    
    def empty(self):
        return len(self.ele) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.ele, (priority, item))
    
    def get(self):
        return heapq.heappop(self.ele)[1]