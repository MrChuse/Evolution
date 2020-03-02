import numpy as np

class Dense:

    def __init__(self, num1, num2, learning_rate=0.01, bias=True):
        self.mt = 2/num1 * np.random.randn(num1, num2) # new weights according to Andrew Ng
        self.bias = np.zeros((1, num2))
        self.lr = learning_rate

    def forward(self, data, bias=True, prnt=False):
        self.x = data.copy()
        t = np.matmul(self.x, self.mt) + (self.bias if bias else 0)
        if prnt:
            print(t, 'dense')
        return t

    def backward(self, dz, bias=True):
        dWeights = np.outer(self.x, dz)
        dx = np.matmul(dz, self.mt.T)
        self.mt -= dWeights * self.lr

        if bias:
            self.bias -= dz * self.lr
        return dx
