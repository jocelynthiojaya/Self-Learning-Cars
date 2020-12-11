import numpy as np
#from scipy.stats import logistic

class ArrayWeights:
    def __init__(self,arr):
        self.arr = arr
        
    def matrixdef(self):
        self.matrix1 = np.reshape(self.arr[:20],(5,4))
        self.matrix2 = np.reshape(self.arr[20:32],(4,3))
        self.matrix3 = np.reshape(self.arr[32:],(3,2))
        return self.matrix1, self.matrix2, self.matrix3
        
        
    
class NeuralNetwork:
    def __init__(self, x):
        self.input = x
        self.output = np.zeros(shape=(1,2))
    
    def sigmoid(self, num):
        value = 1/(1+np.exp(-num))
        return value
        
    def feedforward(self):
        arr = [0,4,2,4,4,2,6,1,6,1,4,5,7,1,3,2,7,2,6,2,5,2,5,
                5,1,5,5,8,3,0,1,2,3,1,2,8,1,9]
        weightmatrix = ArrayWeights(arr)
        self.layer1 = self.sigmoid(np.dot(self.input, weightmatrix.matrixdef()[0]))
        self.layer2 = self.sigmoid(np.dot(self.layer1, weightmatrix.matrixdef()[1]))
        self.output = self.sigmoid(np.dot(self.layer2, weightmatrix.matrixdef()[2]))
        return self.output
    
  
inputvalue = np.array([5,2,3,1,4])
neural1 = NeuralNetwork(inputvalue)
print("output layer: \n", neural1.feedforward())





#print("random weight1: \n",neural1.weight1)
#print("random weight2: \n ",neural1.weight2)
#print(inputvalue.shape)