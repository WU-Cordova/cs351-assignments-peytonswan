class AVLTree(IAVLTREE[K,V] Generic[K, V]):
    def __init__(self):
        self.root = None

    class Node:
        def __init__(self, key, value, height=0):
            self.key = key 
            self.value = value
            self.height = height 
            self.left = None
            self.right = None