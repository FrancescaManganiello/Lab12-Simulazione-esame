import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()      # un grafo non orientato ma pesato
        self._idMap = {}

    # PUNTO 1 ----------------------------------------------------------
    # Richiama il metodo del DAO
    def getRatings(self):
        return DAO.getAllRatings()
    # FINE PUNTO 1 ------------------------------------------------------

    # PUNTO 2 ----------------------------------------------------------
    def buildGraph(self, rating1, rating2):
        self._graph.clear()
        self._actors = DAO.getAllActorsByRange(rating1, rating2)
        for a in self._actors:
            self._idMap[a.ActorID] = a

        self._graph.add_nodes_from(self._actors)

        self._edges = DAO.getAllEdges(rating1, rating2)
        for e1, e2, w in self._edges:
            self._graph.add_edge(self._idMap[e1], self._idMap[e2], weight=w)
            # Il passaggio attraverso self._idMap serve tradurre gli ID del database nei corrispondenti oggetti Nodo
            # creati all'interno del grafo in Python

    # FINE PUNTO 2 -----------------------------------------------------

    # PUNTO 3 ----------------------------------------------------------
    #  Si visualizzino i 5 archi con peso maggiore.
    def get_top_5_archi(self):
        lista_archi = list(self._graph.edges(data=True))
        lista_archi.sort(key=lambda x: x[2]["weight"], reverse=True)

        return lista_archi[0:5]

    # Si visualizzi il numero delle componenti connesse e la componente connessa maggiore.
    def getConnectedComponents(self):
        componenti = list(nx.connected_components(self._graph))
        componente_max = max(componenti, key = len)

        return componenti, componente_max
    # FINE PUNTO 3 -----------------------------------------------------


    def getActors(self):
        return self._graph.nodes()

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())




    # PARTE 2 NON FATTA
    def getBestPath(self):

        self._bestPath = []

        for start in self._graph.nodes():
            partial = [start]
            self._ricorsione(partial)

        return self._bestPath

    def _ricorsione(self, partial):

        if len(partial) > len(self._bestPath):
            self._bestPath = list(partial)

        current = partial[-1]

        for _, successor in self._graph.edges(current):

            # vincolo: età decrescente
            if successor not in partial and successor.birth_date > current.birth_date:
                partial.append(successor)

                self._ricorsione(partial)

                partial.pop()
