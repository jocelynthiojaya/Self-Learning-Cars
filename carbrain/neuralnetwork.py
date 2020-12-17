import numpy as np
from random import random

class NeuralNetwork:
    def __init__(self, x, weights):
        self.input = x
        self.weights = weights
        self.output = np.zeros(shape=(1,2))
        self.matrix1, self.matrix2, self.matrix3 = [[],[],[]]
    
    def sigmoid(self, num):
        value = 1/(1+np.exp(-num))
        return value

    def matrixdef(self, weights):
        self.matrix1 = np.reshape(self.weights[:20],(5,4))
        self.matrix2 = np.reshape(self.weights[20:32],(4,3))
        self.matrix3 = np.reshape(self.weights[32:],(3,2))
        
    def feedforward(self):
        self.matrixdef(self.weights)
        layer1 = np.dot(self.input, self.matrix1)
        layer2 = np.dot(layer1, self.matrix2)
        output = self.sigmoid(np.dot(layer2, self.matrix3)-4)
        return output
    
#arr = [0,4,2,4,4,2,6,1,6,1,4,5,7,1,3,2,7,2,6,2,5,2,5,
#            5,1,5,5,8,3,0,1,2,3,1,2,8,1,9]
arr =  np.array([random() for _ in range(38)])
inputvalue = np.array([random() for _ in range(5)])

neural1 = NeuralNetwork(inputvalue, arr)
#print("input value: \n", inputvalue)
#print("weights array: \n", arr)
print("output layer: \n", neural1.feedforward())

