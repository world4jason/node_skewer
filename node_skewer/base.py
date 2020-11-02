from node_skewer.utils.decorators import cached_property
from abc import ABC, abstractmethod
from typing import Any, List


class Node(ABC):
    """
    The Node interface declares a method for building the chain of nodes.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_successor(self, node):
        pass

    @abstractmethod
    def call(self, request):
        pass


class AbstractNode(Node):
    """
    The default chaining behavior can be implemented inside a base node
    class.
    """
    def __init__(self):
        self.__next_node: Node = None
        self.__name = self.__class__.__name__

    def set_successor(self, node: Node) -> Node:
        self.__next_node = node
        return node

    def call(self, request: Any):
        try:
            response = self.run(request)
        except Exception:
            pass
        if self.__next_node:
            return self.__next_node.call(response)

        return response

    @cached_property
    def name(self):
        return self.__name

    def set_name_prefix(self, prefix):
        self.__name = prefix + "_" + self.__name

    @abstractmethod
    def run(self):
        pass


class FeatureFushionMixin:
    def fushion(self, request : List[Any]):
        return request
