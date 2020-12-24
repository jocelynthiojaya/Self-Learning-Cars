import random
import numpy as np

class geneticAlgorithm:
    def __init__(self, parents1, parents2):
        self.parents1 = []
        self.parents2 = []
        self.child1 = []
        self.child2 = []
        
    def crossover(self):
        if len(self.parents1) == len(self.parents2):
            #check the size of the parents. 
            #get the size of parents 
            sizeParents = len(parents1)
            #generate random number to determine the bound for crossover point 
            crossover_point = random.randint(1,(sizeParents - 1))
            self.child1 = np.concatenate([parents1[0:crossover_point] , parents2[crossover_point:]])
            self.child2 = np.concatenate([parents2[0:crossover_point] , parents1[crossover_point:]])
            
     #def calcfitness(self):
         #fitness = 0

    def mutatiton(self):
        self.crossover()
        #generate the random numbers to find the gene that we want to swap.
        random_numbers = random.randint(0,39)
        self.child1[random_numbers] = random.random()
        self.child2[random_numbers] = random.random()
        return "Child 1 after mutation" ,self.child1, "child 2 after mutation", self.child2 , random_numbers
    
parents1 = np.array([random.random() for _ in range(38)])
parents2 = np.array([random.random() for _ in range(38)])
print("parents1 = " , parents1)
print("parents2 = " , parents2)
g1 = geneticAlgorithm(parents1,parents2)
print(g1.mutatiton())
        
        
        
    
            
            