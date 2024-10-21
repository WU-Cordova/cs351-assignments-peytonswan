from __future__ import annotations 

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple
from datastructures.avltree import AVLTree, AVLNode

class IntervalNode:
    def __init__(self, key, value):
        
        self._key: Tuple[int, int] = key 
        self._value: Any = value 
        self._left: Optional[IntervalNode] = None
        self._right: Optional[IntervalNode] = None 
        self._height: int = 1
        self._max_end: int = value
        self._intervals_at_low: List[IntervalNode] = []
        self._intervals_at_low.append((key[1], value))

    def __str__(self) -> str:
        return f'{self._key, self._value}'
class IntervalTree:
    def __init__(self):
        self._tree = AVLTree()

    def __str__(self) -> str:
        return str(self._tree)

    def insert(self,low: int, high: int, value: Any):
        node: IntervalNode = self._tree.search(low)

        if node: 
            node._intervals_at_low.append(node)

        else:
            new_node = IntervalNode(key=(low,high), value=value)
            new_node._intervals_at_low.append((high, value))
            self._tree.insert(low, new_node)

        self._update_max_end(self._tree.root)

    def _update_max_end(self, node: Optional[IntervalNode]):
        if not node:
            return 0 
        
        left_max = self._update_max_end(node.left)
        right_max = self._update_max_end(node.right)
        max_end = max(left_max, right_max)

        node.max_end = max_end
        return node.max_end
    
    def search(self, low):
        node = self._tree.search(low)
        if node:
            return node._intervals_at_low
        else: 
            return []