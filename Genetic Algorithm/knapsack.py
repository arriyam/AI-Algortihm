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

LOOK INTO TOURNAMENT SELECTION; SEEMS TO BE PICKING THE SAME THING!!!!!! We looked over fitnessgeneration and select2highestparents; they're both good


BestGene:  [0, 1, 0, 1, 1]
Profit:  125
List of items that are selected: ['laptop', 'gold', 'spoon']

here's what the second generation should have:
highest parents:
10011
10011
via tournament selection, here are the winners of the 8 tournaments:
10011


--------------------------------------
IMPORTANT
why is the first element in generation a fitness score of 0. That does not make sense becuase the first 2 genes in generation should only get higher and higher. The mutation function can't change it either

'''
import random

def main():
    n = 5 #total possible items in a single gene
    maxWeight = 10 #max weight
    names = ["pen", "laptop", "hen", "gold", "spoon"]
    profits = [10, 40, 30, 50, 35]
    weights = [5, 4, 6, 3, 2]
    # binArr = [0,0,1,0,1] #random example
    # answer would be items [ laptop, gold, spoon ] [0,1,0,1,1]

    batch = 10 # number of genes in a generation
    size = 0.4 # The percentage value of the amount genes that will be selected in tournment selection
    generationsNumber = 100 # number of generations to be developed
    proabilityOfMutation = 0.3
    
    generation = generateParents(batch, n)
    for generationNumber in range(generationsNumber):

        print(f"GENERATION: {generationNumber}") 
        print()
        print()
        print()
        # print(f"GENERATIONS Array: {generation}")   
        fitnessScores = fitnessGeneration(generation, weights, profits, maxWeight)
        newGeneration = crossOverGeneration(generation, fitnessScores, size, n, batch)
        newGeneration = mutateGeneration(generation, n, batch, proabilityOfMutation)
        generation = newGeneration

    bestGene = bestGeneInGeneration(generation, weights, profits, maxWeight)
    profit = fitness(bestGene, weights, profits, maxWeight)
    namesSelected = itemsSelectedInGene(bestGene, names)
    print("Summary:")
    print(generationsNumber, " generations have been completed")
    print("This is the last Generation: ", newGeneration)
    print("BestGene: ",bestGene)
    print("Profit: ", profit )
    print("List of items that are selected:", namesSelected)



def mutateGeneration(generation, n, batch, proabilityOfMutation):
    for i in range(2,batch-1):
        gene = generation[i]
        bool = random.random() < proabilityOfMutation
        if bool:
            randomIndex = random.randint(0, n-1)
            if gene[randomIndex] == 1:
                gene[randomIndex] = 0
            else:
                gene[randomIndex] = 1
    return generation


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
        
def crossOverGeneration(generation, fitnessScores, size, n, batch):
    profits = [10, 40, 30, 50, 35]
    weights = [5, 4, 6, 3, 2]
    maxWeight = 10
    #print("-"*100)
    #print("Generation Begin",generation)
    #print("Generation Begin Fitness Score", fitnessGeneration(generation, weights, profits, maxWeight))
    #print()
    newGeneration = selectTwoHigestParents(generation, fitnessScores, batch)
    print("HIGHEST SCORE PARENTS IN NEW GENERATION",newGeneration)
    #print("newGeneration Begin", newGeneration)
    #print("newGeneration Begin Fitness Score", fitnessGeneration(newGeneration, weights, profits, maxWeight))
    # print("newGeneration Begin Fitness Score", fitnessGeneration(newGeneration, weights, profits,maxWeight))
    for _ in range(batch-2):
        print("-"*100)
        print("gen before",generation)
        
        gene1, gene2 = tournamentSelection(generation, fitnessScores, size)
        print("highest score genes", gene1, gene2)
        
        print("generation", generation)
        print("fitness scores", fitnessScores)
        print("Fitness gene1, gene2", fitness(gene1, weights, profits, maxWeight), fitness(gene2, weights, profits, maxWeight))
        # print("ben after",generation)
        newGene = crossover(gene1, gene2, n)
    

        newGeneration.append(newGene)
    # print(f"NEW GENERATION: {newGeneration}")
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
        
def itemsSelectedInGene(bestGene, names):
    namesSelected = []
    for i in range(len(bestGene)):
        if bestGene[i] == 1:
            namesSelected.append(names[i])
    return namesSelected

# Helper Function that won't be called in main
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
    
    spliceIndex = random.randint(0,n)
    bool = random.choice([True, False])
    newChild = []
    if bool:
        newChild = gene1[:spliceIndex] + gene2[spliceIndex:]
    else:
        newChild = gene2[:spliceIndex] + gene1[spliceIndex:]
    # print(f"NEW CHILD: {newChild}")
    return newChild


def tournamentSelection(generation, fitnessScores, size):
    modifiableGeneration = generation[:]
    modifiableFitnessScores = fitnessScores[:]
    tournamentSize = int(len(fitnessScores) * size)
    # print("-"*50)
    # print("x: ",modifiableGeneration)
    parents = []
    iterations = 2
    while iterations > 0:
        tournamentMembers = set()
        while len(tournamentMembers) < tournamentSize:
            member = random.randint(0,len(modifiableFitnessScores)-1)
            if member not in tournamentMembers:
                tournamentMembers.add(member) #tournamentMembers = array of indices
                
        # print(f"TOURNAMENT MEMBER: {tournamentMembers}")
        highScore = 0
        remove = -1
        for i in tournamentMembers:
            # print(f"MEMBER {i}: {generation[i]}, {fitnessScores[i]}")
            if modifiableFitnessScores[i] >= highScore:
                remove = i
                highScore = modifiableFitnessScores[i]
        # print(f"TOURNAMENT WINNER: {remove}")
        parents.append(modifiableGeneration[remove])
        del modifiableGeneration[remove]
        del modifiableFitnessScores[remove]
        iterations -= 1
        
    # print("torumnet done")
    # print("crossOverGeneration" , parents[0],parents[1] )
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


        

    
