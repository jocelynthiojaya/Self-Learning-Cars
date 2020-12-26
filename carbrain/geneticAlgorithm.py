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

            #generate random numbers to slice the parents into several parts.
            slice_parents = random.randint(2,sizeParents-1)

            #determine the crossover point. Generate random number to determine the bound for crossover point 
            crossover_array = np.array([random.randint(1,(sizeParents-1)) for _ in range(slice_parents)])
            crossover_array.sort()

            #remove duplicate numbers
            crossover_array = list(dict.fromkeys(crossover_array))
            #count the number of slices again. 
            slice_parents = len(crossover_array)

            #do the crossover
            for i in range(0,slice_parents):
                bounds_top = crossover_array[i]
                #print(bounds_top)
                bounds_low = crossover_array[i-1]
                if len(self.child1) == 0 :
                    self.child1 = np.concatenate([self.child1, parents1[0:bounds_top]])
                    self.child2 = np.concatenate([self.child2, parents2[0:bounds_top]])
                    flag_parents = 1 
                    # if the flag is 1, it will take the value from parents 2 for child 1 and parents 1 for child 2
                elif flag_parents == 1:
                    self.child1 = np.concatenate([self.child1,parents2[bounds_low:bounds_top]])
                    self.child2 = np.concatenate([self.child2, parents1[bounds_low:bounds_top]])
                    flag_parents = 0
                    # if the flag is 0, it will take the value from parents 1 for child 1 and parents 2 for child 2
                elif flag_parents == 0 and len(self.child1) is not 0:
                    self.child1 = np.concatenate([self.child1,parents1[bounds_low:bounds_top]])
                    self.child2 = np.concatenate([self.child2,parents2[bounds_low:bounds_top]])
                    flag_parents = 1

            #ini buat yg belakangnya.
            if flag_parents == 0:
                self.child1 = np.concatenate([self.child1,parents1[bounds_top:]])
                self.child2 = np.concatenate([self.child2,parents2[bounds_top:]])

            elif flag_parents == 1:
                self.child1 = np.concatenate([self.child1,parents2[bounds_top:]])
                self.child2 = np.concatenate([self.child2,parents1[bounds_top:]])
                
        return "child1", self.child1, "child2", self.child2

    def mutatiton(self):
        self.crossover()
        #generate the random numbers to find the gene that we want to swap.
        random_numbers = random.randint(0,39)
        self.child1[random_numbers] = random.random()
        self.child2[random_numbers] = random.random()
        return "Child 1 after mutation" ,self.child1, "child 2 after mutation", self.child2 , random_numbers
    
parents1 = np.array([random.random() for _ in range(38)])
parents2 = np.array([random.random() for _ in range(38)])
#print("parents1 = " , parents1)
#print("parents2 = " , parents2)
g1 = geneticAlgorithm(parents1,parents2)
print(g1.mutatiton())
        
        
        
    
            
            