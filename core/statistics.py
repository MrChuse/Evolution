from collections import defaultdict


class Statistics:
    
    def __init__(self):
        self.dict = defaultdict(list)
    
    def add_tick(self, **tick):
        for key, value in tick:
            self.dict[key].append(value)
   
