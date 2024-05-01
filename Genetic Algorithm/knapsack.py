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

#
            

    

def main():
    n = 5 #total possible items
    w = 10 #max weight
    names = ["pen", "laptop", "hen", "gold", "spoon"]
    profit = [10, 40, 30, 50, 35]
    weight = [5, 4, 6, 3, 2]

    binArr = [0,0,1,0,1] #random example
    # answer would be items [ laptop, gold, spoon ]
    
if __name__ == "__main__":
    main()
