from typing import Any, Callable, Optional, List, TypeVar, Generic

from datastructures.iavltree import IAVLTree

# Define the type variables for the AVL Tree.
K = TypeVar('K')
V = TypeVar('V')

# Node class for the AVL Tree.
class AVLNode(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key  # Node's key
        self.value = value  # Node's value
        self.left = None  # Left child
        self.right = None  # Right child
        self.height = 1  # Initial height is set to 1

# Main AVL Tree class.
class AVLTree(IAVLTree[K, V], Generic[K, V]):
    def __init__(self):
        self.root = None  # Start with an empty root.
        self._size = 0  # Track the number of nodes.

    # Balance Helper Methods for AVLTree Class
    def _get_height(self, node: Optional[AVLNode[K, V]]) -> int:
        """Get the height of the node."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode[K, V]]) -> int:
        """Calculate and return the balance factor of the node."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        """Perform a left rotation on the subtree rooted with `z`."""
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Return new root
        return y

    def _right_rotate(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        """Perform a right rotation on the subtree rooted with `z`."""
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Return new root
        return y

    def _balance(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        """Balance the given node and return the new root of the subtree."""
        balance = self._get_balance(node)

        # If node is left-heavy
        if balance > 1:
            # Left-Right Case
            if self._get_balance(node.left) < 0:
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # If node is right-heavy
        if balance < -1:
            # Right-Left Case
            if self._get_balance(node.right) > 0:
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node


    def insert(self, key: K, value: V) -> None:
        """
        Insert a new key-value pair into the AVL Tree.
        """

        def _insert(node: Optional[AVLNode[K, V]], key: K, value: V) -> AVLNode[K, V]:
            if not node:  # If there's no node, create a new one.
                self._size += 1
                return AVLNode(key, value)

            # Recurse to the correct spot.
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
        
             # Update height and balance the node.
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
            return self._balance(node)  # Balance the node

        self.root = _insert(self.root, key, value)

    def print_tree(self):
        """
        Print the tree in a readable format.
        This will show the keys of the tree in a 'preorder' fashion.
        """
        def _print_tree(node):
            if not node:
                return  # Base case: If the node is None, return.
            
            # Print the current node's key and its children.
            print(f"{node.key}: {node.value}", end=" -> ")
            
            # Print the left and right children recursively.
            _print_tree(node.left)
            _print_tree(node.right)

        # Start printing from the root.
        _print_tree(self.root)
        

    def search(self, key: K) -> Optional[V]:
        """
        Search for a node with the given key and return its value.
        If the key is not found, return None.
        """

        def _search(node: Optional[AVLNode[K, V]], key: K) -> Optional[V]:
            """
            Internal helper function to search for a node.
            Args:
            - node: The current node we are looking at.
            - key: The key of the node to search for.
            Returns: The value if found, or None if not found.
            """
            if not node:  # Base case: If we reach an empty spot, the key does not exist.
                return None

            if key < node.key:  # If the key is smaller, go to the left child.
                return _search(node.left, key)
            elif key > node.key:  # If the key is larger, go to the right child.
                return _search(node.right, key)
            else:  # If the key matches, return the value.
                return node.value

        # Start the search from the root node.
        return _search(self.root, key)
    
    def delete(self, key: K) -> None:
        """
        Delete a node with the given key.
        """

        def _delete(node: Optional[AVLNode[K, V]], key: K) -> Optional[AVLNode[K, V]]:
            """
            Internal helper function to delete a node.
            Args:
            - node: The current node we are looking at.
            - key: The key of the node to delete.
            Returns: The updated node.
            """
            if not node:  # If we reach an empty spot, the key is not in the tree.
                return node

            if key < node.key:  # If the key is smaller, go to the left child.
                node.left = _delete(node.left, key)
            elif key > node.key:  # If the key is larger, go to the right child.
                node.right = _delete(node.right, key)
            else:
                # We found the node to delete.

                # Case 1: Node has no left child.
                if not node.left:
                    return node.right  # Replace with right child.

                # Case 2: Node has no right child.
                elif not node.right:
                    return node.left  # Replace with left child.

                # Case 3: Node has two children.
                # Get the inorder successor (smallest node in the right subtree).
                temp = self._get_min_value_node(node.right)
                node.key, node.value = temp.key, temp.value  # Copy the inorder successor's key and value.
                node.right = _delete(node.right, temp.key)  # Delete the inorder successor.

            # Update height and balance the node.
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
            return self._balance(node)  # Balance the node

        self.root = _delete(self.root, key)

        # Start the deletion from the root node.
        # self.root = _delete(self.root, key)

    def _get_min_value_node(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        """
        Get the node with the smallest key (left-most child).
        """
        current = node
        while current.left:  # Keep going left until you find the smallest key.
            current = current.left
        return current

    def inorder(self, visit: Callable[[V], None] | None = None) -> List[K]:

        def _inorder(node):
            if not node:
                return 
            
            _inorder(node.left)
           # if visit: 
            # visit(node.value)
            
            keys.append(node.key)

            _inorder(node.right)
            
        
        keys = []
        _inorder(self.root)
        return keys 
        

    def preorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        
        def _preorder(node):
            if not node:
                return
            
            #if visit:
                #visit(node.value)
            keys.append(node.key)
            _preorder(node.left)
            _preorder(node.right)

        keys = []
        _preorder(self.root)
        return keys 

    def postorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        result: List[K] = []

        def _postorder(node: Optional[AVLNode[K, V]]):
            if not node:
                return
            _postorder(node.left)  # Traverse the left subtree.
            _postorder(node.right)  # Traverse the right subtree.
            result.append(node.key)  # Visit the root node.
            if visit:
                visit(node.value)

        _postorder(self.root)
        return result

    def bforder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        result: List[K] = []
        queue = [self.root] if self.root else []  # Initialize the queue with the root node.

        while queue:
            node = queue.pop(0)  # Remove the front element from the queue.
            if node:
                result.append(node.key)  # Visit the node.
                if visit:
                    visit(node.value)
                queue.append(node.left)  # Add the left child to the queue.
                queue.append(node.right)  # Add the right child to the queue.

        return result

    def size(self) -> int:
        return self._size

    def __str__(self) -> str:
        def draw_tree(node: Optional[AVLNode], level: int=0) -> None:
            if not node:
                return 
            draw_tree(node.right, level + 1)
            level_outputs.append(f'{" " * 4 * level} -> {str(node.value)}')
            draw_tree(node.left, level + 1)
        level_outputs: List[str] = []
        draw_tree(self.root)
        return '\n'.join(level_outputs)
    
    def __repr__(self) -> str:
        #descriptions = ['Breadth First: ', 'In-order: ', 'Pre-order: ', 'Post-order: ']
        #traversals = [self.bforder(), self.inorder(), self.preorder(), self.postorder()]
        #return f'{"\n".join([f'{desc} {"".join(str(trav))}' for desc, trav in zip(descriptions, traversals)])}\n\n{str(self)}' 
        keys = self.preorder(self.root)
        output = "preorder" + repr(keys)

        keys = self.inorder(self.root)
        output+="inorder" + repr(keys)

        return output
# Test the implementation.
tree = AVLTree()
tree.insert("Alice", 24)
tree.insert("Bob", 30)
tree.insert("Charlie", 28)
print(repr(tree))
#tree.print_tree()

#print(tree.search("Bob"))  # Output: 30 (found the value 30 for key "Bob")

# Search for "Alice".
#print(tree.search("Alice"))  # Output: 24 (found the value 24 for key "Alice")

#key that doesn’t exist.
#print(tree.search("David"))  # Output: None (David is not in the tree)

#tree.delete("Bob")


#tree.print_tree()