import flet as ft
from geopy import distance

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        anni=self._model.dd_a()
        self._view.dd_year.options.clear()
        for anno in anni:
            self._view.dd_year.options.append(ft.dropdown.Option(text=str(anno)))
        self._view.update()

    def populate_dd_f(self,e):
        anno=self._view.dd_year.value
        forme=self._model.dd_f(anno)
        self._view.dd_shape.options.clear()
        for forma in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(text=str(forma)))
        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        anno = self._view.dd_year.value
        forma=self._view.dd_shape.value
        self._model.build_graph(anno,forma)
        peso_nodo = self._model.nodo_peso()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Numero di vertici: {self._model.G.number_of_nodes()} Numero di archi: {self._model.G.number_of_edges()}"))
        for nodo,peso in peso_nodo:
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Nodo {nodo}, somma pesi su archi={peso}"))
        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        percorso,distanza=self._model.get_percorso_migliore()
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Peso cammino massimo: {distanza}"))

        for i in range(len(percorso)-1):
            stato1=percorso[i]
            stato2=percorso[i+1]
            w=self._model.G[stato1][stato2]['weight']
            distanza_km=distance.geodesic((stato1.lat, stato1.lng), (stato2.lat, stato2.lng)).km
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f"{stato1.id} --> {stato2.id}: weight {w} distance {distanza_km}"))
        self._view.update()

