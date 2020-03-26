import numpy as np

class Tanh:
        
    def forward(self, data, prnt=False):
        self.x = data.copy()
        self.x = np.exp(2 * self.x)
        self.x = (self.x-1) / (self.x+1)
        if prnt:
            print(self.x, 'tanh')
        return self.x
    
    def backward(self, loss):
        return loss * (1 - self.x * self.x)