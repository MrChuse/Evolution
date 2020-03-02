import numpy as np

class ReLU:
    def forward(self, x):
        self.x = x
        self.x[self.x < 0] = 0
        return self.x
    
    def backward(self, loss):
        loss[self.x <= 0] = 0
        return loss
        
        
if __name__ == '__main__':
    a = ReLU()
    x = np.array([-1, 2, 3, 4])
    print(a.forward(x))
    print(x)
