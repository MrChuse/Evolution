import numpy as np

class mse:
    def forward(self, x, y):
        self.x = x
        self.y = y
        return np.square(self.x - self.y).mean()
        
    def backward(self):
        return 2 * (self.x - self.y)