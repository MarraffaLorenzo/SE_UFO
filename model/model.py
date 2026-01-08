import networkx as nx
from geopy import distance
from database.dao import DAO
class Model:
    def __init__(self):
        self.lista_anni=[]
        self.lista_forme=[]
        self.G=nx.Graph()
        self.nodes=[]
        self.dict_nodes={}
        self.archi=[]
        self.percorso_migliore=[]
        self.peso_migliore=0

    def dd_a(self):
        self.lista_anni=[]
        anni=DAO.get_anni()
        for anno in anni:
            self.lista_anni.append(anno)

        return self.lista_anni

    def dd_f(self,anno):
        self.lista_forme=[]
        forme=DAO.get_forme(anno)
        for forma in forme:
            self.lista_forme.append(forma)

        return self.lista_forme

    def build_graph(self,anno,forma):
        self.G.clear()
        self.nodes=[]
        self.dict_nodes={}
        self.archi=[]
        nodi=DAO.get_nodes()
        for nodo in nodi:
            self.nodes.append(nodo)
            self.dict_nodes[nodo.id.upper()]=nodo
        self.G.add_nodes_from(self.nodes)
        archi=DAO.get_archi_stati()
        stato_peso=DAO.get_pesi(anno,forma)
        for id1,id2 in archi:
            stato1=self.dict_nodes.get(id1.upper())
            stato2=self.dict_nodes.get(id2.upper())
            if stato1 and stato2 :
                w1=stato_peso.get(id1.upper(),0)
                w2=stato_peso.get(id2.upper(),0)
                peso_totale=w1+w2
                self.G.add_edge(stato1,stato2,weight=peso_totale)


    def nodo_peso(self):
        result=[]
        for nodo in self.G.nodes():
            peso=self.G.degree(nodo,weight="weight")
            result.append((nodo.id,peso))
        return result

    def get_percorso_migliore(self):
        self.percorso_migliore.clear()
        self.peso_migliore=0
        for n in self.G.nodes():
            parziale=[n]
            self.ricorsione(parziale,-1,0)

        return self.percorso_migliore,self.peso_migliore

    def ricorsione(self,parziale,ultimo_peso,distanza):
        ultimo=parziale[-1]
        if distanza>self.peso_migliore:
            self.peso_migliore=distanza
            self.percorso_migliore=parziale.copy()

        vicini = self.G.neighbors(ultimo)

        for vicino in vicini:
            peso_arco=self.G[ultimo][vicino]["weight"]
            if vicino in parziale:
                continue
            if peso_arco>ultimo_peso:
                distanza_geodesic=distance.geodesic((ultimo.lat,ultimo.lng),(vicino.lat,vicino.lng)).km
                parziale.append(vicino)

                self.ricorsione(parziale,peso_arco,distanza_geodesic+distanza)
                parziale.pop()







