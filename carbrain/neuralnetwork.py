import numpy as np
from scipy.stats import logistic

class NeuralNetwork:
    def __init__(self,x):
        self.inputlayer = x
        self.weight1 = np.random.randint(10, size=5)
        self.weight2 = np.random.randint(10, size=2)
        self.outputlayer = np.zeros(shape=(1,2))
    
    def feedforward(self):
        self.layer1 = 2 * (logistic.cdf(np.dot(self.inputlayer,self.weight1)))-1
        self.outputlayer = 2 *(logistic.cdf(np.dot(self.layer1,self.weight2)))-1
        return self.outputlayer
    
      
inputvalue = np.array([-1,-1,0,1,1])
neural1 = NeuralNetwork(inputvalue)
print("output layer", neural1.feedforward())
print("random weight1 ",neural1.weight1)
print("random weight2 ",neural1.weight2)





        
