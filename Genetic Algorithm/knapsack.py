'''

Input: N = 3, W = 4, profit[] = {1, 2, 3}, weight[] = {4, 5, 1}
Output: 3
Explanation: There are two items which have weight less than or equal to 4. If we select the item with weight 4, the possible profit is 1. And if we select the item with weight 1, the possible profit is 3. So the maximum possible profit is 3. Note that we cannot put both the items with weight 4 and 1 together as the capacity of the bag is 4.

Input: N = 3, W = 3, profit[] = {1, 2, 3}, weight[] = {4, 5, 6}
Output: 0



child = [0 0 0 1 0 0 0 0 0 0]

'''

# def createContents():
    

def main():
    n = 5
    w = 10
    names = ["pen", "laptop", "hen", "gold", "spoon"]
    profit = [10, 40, 30, 50, 35]
    weight = [5, 4, 6, 3, 2]
    # answer would be items [ laptop, gold, spoon ]

class Sack:
    def __init__(contents):
        self.contents = contents

        self._weight = 0
        self._profit = 0
        for item in contents:
            self.weight +=  item.weight
            self.profit +=  item.profit
        
    def getSackWeight():
        return(self._weight)
    
    def getSackProfit():
        return(self._profit)

class SackItem:
    def __init__(name, weight, profit):
        self._name = name
        self._weight = weight
        self._profit = profit

    def getName():
        return(self._name)
    
    def getItemWeight():
        return(self._weight)
    
    def getItemProfit():
        return(self._profit)
    
    def displayItem(self):
        print(f"Item name: {self._name}, weight: {self._weight}, profit: {self._profit}")
    
if __name__ == "__main__":
    main()
