from node_skewer.base import AbstractNode, FeatureFushionMixin
from abc import abstractmethod


class AbstractFlow(AbstractNode):
    """
    Graph + Chain of Responsibililty

    """
    def __init__(self, graph=None):
        assert isinstance(graph, dict)

        self.__graph = graph
        self.__vertices_names, self.__vertices = zip(*self.__graph.items())

        super().__init__()
        self._build()

    def _validate_vertices(self):
        for v in self.vertices:
            if not (hasattr(v, "run")):
                raise TypeError("All Node should implement run "
                                " '%s' (type %s) doesn't" % (v, type(v)))

    def _build(self):
        """
        Design Pattern : builder
        """
        self.build()

        # set prefix
        [v.set_name_prefix(self.name) for v in self.vertices]

        self._validate_vertices()
        return self

    @abstractmethod
    def build(self):
        """
        transform value for init
        """
        pass

    def run(self, request=None, start_node=None):
        """A client that calls node(handler)"""
        response = self.vertices[0].call(request)
        return response

    def graph(self):
        return self.__graph

    @property
    def vertices(self):
        """ returns the vertices of a graph """
        return self.__vertices

    def set_vertices(self, vertices):
        """ returns the vertices of a graph """
        self.__vertices = vertices

    def plot(self):
        from graphviz import Digraph

        dot = Digraph(comment=self.name)
        vertices = self.vertices

        for idx in range(len(vertices)):
            dot.node(vertices[idx].name)
            if idx > 0:
                dot.edge(vertices[idx - 1].name, vertices[idx].name)

        dot.format = 'png'
        dot.render('output-graph', view=True)


class Pipe(AbstractFlow):
    """
    Graph + Chain of Responsibililty

    """

    def init(self):
        pass

    def build(self):
        vertices = self.vertices
        for idx in range(len(vertices) - 1):
            vertices[idx].set_successor(vertices[idx + 1])

    def run(self, request=None, start_node=None):
        """A client that calls node(handler)"""
        response = self.vertices[0].call(request)
        return response

    def plot(self):
        from graphviz import Digraph

        dot = Digraph(comment=self.name)

        vertices = self.vertices
        for idx in range(len(vertices)):
            dot.node(vertices[idx].name)
            if idx > 0:
                dot.edge(vertices[idx - 1].name, vertices[idx].name)

        dot.format = 'png'
        dot.render('output-graph', view=True)


class Union(FeatureFushionMixin, AbstractFlow):
    """
    Graph + Chain of Responsibililty
    """

    def __init__(self, graph):
        super().__init__(graph)

    def build(self):
        """
        response should merge by Union
        which mean no successor for each vertice
        """
        self.set_vertices(self.vertices[0])
        [vertice.set_successor(None) for vertice in self.vertices]

    def run(self, request=None, start_node=None, multiprocessing=False):
        """Basically this is a union node"""
        if multiprocessing:
            import multiprocessing
            # TODO: multiprocessing

        else:
            response = [vertice.call(request) for vertice in self.vertices]
        response = super().fushion(response)
        return response

    def plot(self):
        from graphviz import Digraph

        dot = Digraph(comment=self.name)

        vertices = self.vertices
        for idx in range(len(vertices)):
            dot.node(vertices[idx].name)

        dot.format = 'png'
        dot.render('output-graph', view=True)
