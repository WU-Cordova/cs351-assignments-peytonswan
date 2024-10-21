from dataclasses import dataclass
from datastructures.avltree import AVLTree
from datastructures.intervaltree import IntervalTree



@dataclass(order = True)
class Stock:
    symbol: str
    name: str
    low: int
    high: int

    def __str__(self) -> str:
        return f'stock {self.symbol} {self.name} {self.low} {self.high}'
    
   
class StockManager:
    def __init__(self) -> None:
        self._interval_tree = IntervalTree()
        with open('Stocks\\sample_stock_prices.csv', "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i == 0: continue 
                data = line.split(',')
                symbol = data[0]
                name = data[1]
                low = int(data[2].strip())
                high = int(data[3].strip())
                stock = Stock(symbol, name, low, high)
                self._interval_tree.insert(low, high, stock)
    
    
        print(self._interval_tree)

    def search(self, low):
        return self._interval_tree.search(low)


stockmanager = StockManager()