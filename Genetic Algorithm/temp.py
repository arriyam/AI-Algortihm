import random





def crossover(gene1, gene2, n):
    spliceIndex = random.randint(0,n)
    print("Splice index: ", spliceIndex)
    bool = random.choice([True, False])
    bool = True
    newChild = []
    if bool:
        newChild = gene1[:spliceIndex] + gene2[spliceIndex:]
    else:
        newChild = gene2[:spliceIndex] + gene1[spliceIndex:]
    # print(f"NEW CHILD: {newChild}")
    return newChild

n =5
gene1 = [1,2,3,4,5]
gene2 = [6,7,8,9,10]

#print("Gene1", gene1)
#print("Gene2", gene2)
for i in range(20):
    print("-"*100)
    print("Gene1", gene1)
    print("Gene2", gene2)
    print("Crossover", crossover(gene1,gene2,n))