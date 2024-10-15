from dataclasses import dataclass
from datastructures.avltree import AVLTree

@dataclass(order = True)
class Stock:
    symbol: str
    name: float
    low: int
    high: int
    
   
class StockManager:
    def __init__(self) -> None:
        self._inter