from __future__ import annotations 
from datastructures import AVLTree 
from dataclasses import dataclass
from typing import Any, Optional, Tuple

@dataclass
class IntervalNode:
    key: Tuple[int, int]
    value: Any
    left: Optional[IntervalNode] = None
    right: Optional[IntervalNode] = None
    height: int = 3
    max_end: int = 0
    intervals_at_low: AVLTree = AVLTree()

class IntervalTree:
    def __init__(self):
        self._tree = AVLTree()

    def insert(self,low: int, high: int, value: Any):
        node = IntervalNode = self._tree.search(low)

        if node:
            node.intervals_at_low.insert(high, value)

        else:
            new_node = IntervalNode(key=(low,high), value=value, max_end=high)
            new_node.intervals_at_low.insert(high, value)
            self._tree.insert(low, new_node)

        self._update_max_end(self._tree._root)

    def _update_max_end(self, node: Optional[IntervalNode]):
        if not node:
            return 0 
        
        left_max = self._update_max_end(node.left)
        right_max = self._update_max_end(node.right)
        max_end = max(left_max, right_max)

        node.max_end = max_end
        return node.max_end