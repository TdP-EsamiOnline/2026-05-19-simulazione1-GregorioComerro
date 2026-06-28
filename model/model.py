import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artists = []


    def buildGraph(self, idGenre):
        self._graph.clear()
        self._artists = DAO.getAllNodes(idGenre)

        for artist in self._artists:
            self._graph.add_node(artist)

        edges = DAO.getAllEdges(idGenre)
        popolarita = DAO.getPopularities(idGenre)

        idMap = {}
        for artist in self._artists:
            idMap[artist.ArtistId] = artist

        for id1, id2 in edges:
            artist1 = idMap[id1]
            artist2 = idMap[id2]

            pop1 = popolarita[id1]
            pop2 = popolarita[id2]

            peso = pop1 + pop2

            if pop1 > pop2:
                self._graph.add_edge(artist1, artist2, weight=peso)
            elif pop2 > pop1:
                self._graph.add_edge(artist2, artist1, weight=peso)
            else:
                self._graph.add_edge(artist1, artist2, weight=peso)
                self._graph.add_edge(artist2, artist1, weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        archi = list(self._graph.edges(data=True))

        archi.sort(key=lambda x: x[2]["weight"], reverse=True)

        return archi[:5]

    def getInfluenza(self, artist):
        pesoUs = 0
        pesoEn = 0
        for _, _, dati in self._graph.out_edges(artist, data=True):
            pesoUs += dati["weight"]

        for _, _, dati in self._graph.in_edges(artist, data=True):
            pesoEn += dati["weight"]
        return pesoUs-pesoEn



    def getArtistMaxInfluence(self):
        bestArtist = None
        maxInfluence = None

        for artist in self._graph.nodes:
            influence = self.getInfluenza(artist)

            if maxInfluence is None or influence > maxInfluence:
                bestArtist = artist
                maxInfluence = influence

        return bestArtist, maxInfluence





    def getAllGenres(self):
        return DAO.getAllGenres()