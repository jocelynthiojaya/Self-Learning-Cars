import numpy as np
#from scipy.stats import logistic

class NeuralNetwork:
    def __init__(self, x):
        self.input = x
        self.weight1 = np.random.rand(5, 4)
        self.weight2 = np.random.rand(4, 3)
        self.weight3 = np.random.rand(3, 2)
        self.output = np.zeros(shape=(1,2))
    
    def sigmoid(self, num):
        value = 1/(1+np.exp(-num))
        return value

    def feedforward(self):
        self.layer1 = self.sigmoid(np.dot(self.input, self.weight1))
        self.layer2 = self.sigmoid(np.dot(self.layer1, self.weight2))
        self.output = self.sigmoid(np.dot(self.layer2, self.weight3))
        return self.output
    
  
inputvalue = np.array([5,2,3,1,4])
neural1 = NeuralNetwork(inputvalue)
print("output layer: \n", neural1.feedforward())
#print("random weight1: \n",neural1.weight1)
#print("random weight2: \n ",neural1.weight2)
#print(inputvalue.shape)