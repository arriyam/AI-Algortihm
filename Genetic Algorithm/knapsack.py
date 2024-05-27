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
    # binArr = [0,0,1,0,1] #random example
    # answer would be items [ laptop, gold, spoon ]

    batch = 5 # Should be above equal to 5
    size = 0.4 # The percentage value of the amount genes that will be selected in tournment selection
    generations = 2 # number of generations to be developed
    
    
    generation = generateParents(batch, n)
    for generationNumber in range(generations):
        print(f"GENERATION: {generationNumber}") 
        print(f"GENERATION Index: {generation}")   
        fitnessScores = fitnessGeneration(generation, weights, profits, maxWeight)
        newGeneration = crossOverGeneration(generation, fitnessScores, size, n)
        generation = newGeneration

    print(generations, " generations have been completed")
    print("This is the last Generation' ", newGeneration)
    bestGene = bestGeneInGeneration(generation, weights, profits, maxWeight)
    print("BestGene:",bestGene)


#randomly generate first generation (parents)
def generateParents(batch,n):
    generation = []
    generation.append([1]*n) #first parent = all 1s

    for _ in range(1,batch): # 2nd parent to batch size
        parent = [random.choice([0, 1]) for _ in range(n)]
        generation.append(parent)

    return generation
        
def fitnessGeneration(generation, weights, profits, maxWeight):
    fitnessScores = []
    for gene in generation:
        fitnessScore = fitness(gene, weights, profits, maxWeight)
        fitnessScores.append(fitnessScore)
    return fitnessScores
        
def crossOverGeneration(generation, fitnessScores, size, n):
    newGeneration = selectTwoHigestParents(generation, fitnessScores, n)
    for i in range(n-2):
        a = i + 1
        gene1, gene2 = tournamentSelection(generation, fitnessScores, size)
        newChild = crossover(gene1, gene2, n)
        newGeneration.append(newChild)
    print(f"NEW GENERATION: {newGeneration}")
    return newGeneration

def bestGeneInGeneration(generation, weights, profits, maxWeight):
    bestGene = generation[0]
    bestProfit = fitness(generation[0], weights, profits, maxWeight)

    for i in range(1,len(generation)):
        gene = generation[i]
        geneProfit = fitness(generation[i], weights, profits, maxWeight)
        if geneProfit > bestProfit:
            bestGene = gene
            bestProfit = geneProfit   
    return bestGene
        


# Helper Function that won't be called in main

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

def findTwoHighestIndices(fitnessScores,n):
    index1, index2 = (0, 1) if fitnessScores[0] > fitnessScores[1] else (1, 0)
    
    for i in range(2, n):
        if fitnessScores[i] > fitnessScores[index1]:
            index2 = index1
            index1 = i
        elif fitnessScores[i] > fitnessScores[index2]:
            index2 = i

    return index1, index2

def selectTwoHigestParents(generation, fitnessScores, n):
    newGeneration = []

    highestGeneIndex, SecondHighestGeneIndex = findTwoHighestIndices(fitnessScores,n)
    newGeneration.extend([generation[highestGeneIndex], generation[SecondHighestGeneIndex]])
    return newGeneration

def crossover(gene1, gene2, n):
    spliceIndex = random.randint(2,n-2)
    bool = random.choice([True, False])
    newChild = []
    if bool:
        newChild = gene1[:spliceIndex] + gene2[spliceIndex:]
    else:
        newChild = gene2[:spliceIndex] + gene1[spliceIndex:]
    print(f"NEW CHILD: {newChild}")
    return newChild

def tournamentSelection(generation, fitnessScores, size):
    tournamentSize = int(len(fitnessScores) * size)
    # print(tournamentSize)
    parents = []
    iterations = 2
    while iterations > 0:
        tournamentMembers = set()
        while len(tournamentMembers) < tournamentSize:
            member = random.randint(0,len(fitnessScores)-1)
            if member not in tournamentMembers:
                tournamentMembers.add(member) #tournamentMembers = array of indices
                
        # print(f"TOURNAMENT MEMBER: {tournamentMembers}")
        highScore = 0
        remove = -1
        for i in tournamentMembers:
            # print(f"MEMBER {i}: {generation[i]}, {fitnessScores[i]}")
            if fitnessScores[i] >= highScore:
                remove = i
                highScore = fitnessScores[i]
        # print(f"TOURNAMENT WINNER: {remove}")
        parents.append(generation[remove])
        del generation[remove]
        del fitnessScores[remove]
        iterations -= 1
        
    # print("torumnet done")
    return parents[0], parents[1]

if __name__ == "__main__":
    main()


'''
    
    n = 5
    Highest 2 goes to the next generation
    Remove the 2 lowests
    first generation:  [c1,c2,c3,c4,c5] lowest to higest

    ^^^
    1. size = 0.60*len(arr) (0.60*5) = 3
    2. randomly generate 3 indices i,j,k between 0 and len(arr)
    3. save parent (e.g., generation[i]) whose fitness score is highest, remove from generation array
    4. repeat 1, 2, and 3
    5. return 2 parents


    second generation: [c23,c34,c45,c4,c5] not in order

    first generation:  [c1,c2,c3,c4,c5, c6] lowest to higest

    second generation: [c23,c34,c45,c56,c5, c6] not in order

'''


        

       
