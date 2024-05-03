'''

Input: N = 3, W = 4, profit[] = {1, 2, 3}, weight[] = {4, 5, 1}
Output: 3
Explanation: There are two items which have weight less than or equal to 4. If we select the item with weight 4, the possible profit is 1. And if we select the item with weight 1, the possible profit is 3. So the maximum possible profit is 3. Note that we cannot put both the items with weight 4 and 1 together as the capacity of the bag is 4.

Input: N = 3, W = 3, profit[] = {1, 2, 3}, weight[] = {4, 5, 6}
Output: 0


child = [0 0 0 1 0 0 0 0 0 0]

List of things we need:

1. genetic representation of a solution
2. a function to generate new solutions
3. fitness function
4. selection function
5. crossover function
6. mutation function2


Tomorrow:

create mutation function

Run the evolution
'''
import random

def main():
    n = 5 #total possible items
    maxWeight = 10 #max weight
    names = ["pen", "laptop", "hen", "gold", "spoon"]
    profits = [10, 40, 30, 50, 35]
    weights = [5, 4, 6, 3, 2]
    binArr = [0,0,1,0,1] #random example
    # answer would be items [ laptop, gold, spoon ]

    batch = 5 # Should be above equal to 5
    generation = generateParents(batch,n)
    fitnessScores = fitnessGeneration(generation, weights, profits, maxWeight)

    newGeneration = selectionAndCrossover(generation, fitnessScores, n)

    print("Initial Generation:", generation)

    print("New Generation:", newGeneration)
    
     

#randomly generate first generation (parents)
def generateParents(batch,n):
    generation = []
    generation.append([1]*n) #first parent = all 1s

    for _ in range(1,batch): # 2nd parent to batch size
        parent = [random.choice([0, 1]) for _ in range(n)]
        generation.append(parent)

    return generation
        

#return the fitness score for a gene (parent or child)
def fitness(gene, weights, profits, maxWeight):
    geneWeight = 0
    geneProfit = 0
    for i in range(len(gene)):
        if gene[i]==1:
            geneWeight += weights[i]
            geneProfit += profits[i]

    if geneWeight <= maxWeight:
        return geneProfit

    return 0

def fitnessGeneration(generation, weights, profits, maxWeight):
    fitnessScores = []
    for gene in generation:
        fitnessScore = fitness(gene, weights, profits, maxWeight)
        fitnessScores.append(fitnessScore)
    return fitnessScores

def selectionAndCrossover(generation, fitnessScores, n):
    #for n iterations, run tournament with x random parents, use 2 tournament winners as parents, randomly split parent genes into child gene, mutate a bit
    '''
    n = 5
    Highest 2 goes to the next generation
    Remove the 2 lowests
    first generation:  [c1,c2,c3,c4,c5] lowest to higest

    second generation: [c23,c34,c45,c4,c5] not in order

    first generation:  [c1,c2,c3,c4,c5, c6] lowest to higest

    second generation: [c23,c34,c45,c56,c5, c6] not in order
    
    '''

    paired_data = list(zip(fitnessScores, generation))
    # Sorting the paired data by fitness scores in ascending order
    sorted_data = sorted(paired_data)
    paired_data.sort()
    print(paired_data)
    print(sorted_data)

    newGeneration = []
    highestGeneIndex, SecondHighestGeneIndex = findTwoHighestIndices(fitnessScores,n)
    newGeneration.extend([generation[highestGeneIndex], generation[SecondHighestGeneIndex]])
    for i in range(n-2):
        a = i + 1
        c1, c2 = generation[i], generation[a]
        spliceIndex = random.randint(2,n-2)
        bool = random.choice([True, False])
        newChild = []
        if bool:
            newChild = c2[:spliceIndex] + c1[spliceIndex:]
        else:
            newChild = c1[:spliceIndex] + c2[spliceIndex:]
        newGeneration.append(newChild)

    return newGeneration
        

       
def findTwoHighestIndices(fitnessScores,n):
    index1, index2 = (0, 1) if fitnessScores[0] > fitnessScores[1] else (1, 0)
    
    for i in range(2, n):
        if fitnessScores[i] > fitnessScores[index1]:
            index2 = index1
            index1 = i
        elif fitnessScores[i] > fitnessScores[index2]:
            index2 = i

    return index1, index2

    


if __name__ == "__main__":
    main()
