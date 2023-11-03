'''A basic Linked List structure with some custom methods.


Author:

    Ronit Samanta

Classes:

    Node

'''


from sys import setrecursionlimit
setrecursionlimit(100_000)
del setrecursionlimit


class Node:
    '''A class combining a Linked List and its Nodes


    Methods:

        add_node(next_node)

        set_path(path)

        cut_nodes_at(value_to_remove, depth_to_remove, keep)

        get_value_at(depth) -> str

        get_depth_of(value) -> int

        get_max_depth() -> int

        as_list(include) -> list[str]


    Attributes:

        value,

        next,

        depth,

        is_root

    '''

    def __init__(self, value: str, depth: int, is_root: bool = False) -> None:
        '''
        :param value - the value the Node holds
        :param depth - the depth at which the Node rests
        :param (optional) is_root - whether the Node is the root
            Note: in the methods where is_root is used, the
            functionality may be faulty if a non-root Node has is_root
            set to True
        '''

        self.value = value
        self.next = None
        self.depth = depth
        self.is_root = is_root

    def add_node(self, next_node: str) -> None:
        '''Adds node to end of Linked List'''

        if self.next is None:
            self.next = Node(next_node, self.depth + 1)
        else:
            self.next.add_node(next_node)

    def set_path(self, path: str | list[str]) -> None:
        '''Constructs new Linked List and assigns to self

        :param path - string or list[str] representation of Node object
        '''

        if not self.is_root:
            return
        if isinstance(path, str):
            path = path.split(' -> ')

        self.cut_nodes_at(depth_to_remove=0)
        self.value = path[0]
        for word in path[1:]:
            self.add_node(word)

    def cut_nodes_at(self, value_to_remove: str = None, depth_to_remove: int = None, keep: bool = False) -> None:
        '''Separates part of Linked List at either value or depth

        :param value_to_remove - if provided, str value will be searched
            for and removed, cutting off all Nodes connected
        :param depth_to_remove - if provided, Node at depth will be
            removed, cutting off all Nodes connected
        :param keep - whether or not the Node at value or depth is to
            remain
        '''

        if value_to_remove is not None:
            value_to_remove = value_to_remove.upper()
            self.cut_nodes_at(
                depth_to_remove=self.get_depth_of(value_to_remove), keep=keep)

        if depth_to_remove is not None:
            if keep:
                depth_to_remove += 1
            if depth_to_remove == 0:
                depth_to_remove = 1
            elif depth_to_remove < 0:
                depth_to_remove += self.get_max_depth()
            if self.next is None:
                return
            elif self.next.depth == depth_to_remove:
                self.next = None
            else:
                self.next.cut_nodes_at(None, depth_to_remove)

    def get_value_at(self, depth: int) -> str:
        '''Returns value of Node at given depth'''

        if depth < 0:
            depth += self.get_max_depth() + 1

        if self.depth == depth:
            return self.value
        elif self.next is None:
            return None
        else:
            return self.next.get_value_at(depth)

    def get_depth_of(self, value: str) -> int:
        '''Returns depth of Node that contains given value'''

        if self.value == value:
            return self.depth
        elif self.next is None:
            return None
        else:
            return self.next.get_depth_of(value)

    def get_max_depth(self) -> int:
        '''Returns the depth of the last Node'''

        if self.next is None:
            return self.depth

        return self.next.get_max_depth()

    def __str__(self) -> str:
        out = f'{self.value}'
        if self.next is not None:
            out += ' -> ' + str(self.next)
        return out

    def __len__(self) -> int:
        return len(self.as_list())

    def as_list(self, include: bool = False) -> list[str]:
        '''Returns list representationo of Linked List

        :param include - whether or not to include the starting word
        '''

        return str(self).split(' -> ')[(0 if include else 1):]
