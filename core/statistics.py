from collections import defaultdict


class Statistics:
    
    def __init__(self):
        self.dict = defaultdict(list)

    def __getitem__(self, item):
        return self.dict[item]

    def __len__(self):
        return len(next(iter(self.dict.values())))
    
    def add_tick(self, **tick):
        for key, value in tick.items():
            self.dict[key].append(value)
