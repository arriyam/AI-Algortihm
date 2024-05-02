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

    print(generation)
    fitnessScores=[]
    for gene in generation:
        fitnessScore = fitness(gene, weights, profits, maxWeight)
        fitnessScores.append(fitnessScore)
    print(fitnessScores)
    
     

#randomly generate first generation (parents)
def generateParents(batch,n):
    generation = []
    generation.append([1]*n) #first parent = all 1s

    for _ in range(1,batch): # 2nd parent to batch size
        parent = [random.choice([0, 1]) for _ in range(n)]
        generation.append(parent)

    return(generation)
        

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


    


if __name__ == "__main__":
    main()
