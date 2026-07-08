import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # PUNTO 1 ----------------------------------------------------------
    # Metodo per riempire il dropdown
    def fillDDsRating(self):
        ratings = self._model.getRatings()

        ratingsDD = list(map(lambda x: ft.dropdown.Option(x), ratings))
        self._view._ddrating1.options = ratingsDD
        self._view._ddrating2.options = ratingsDD
        self._view.update_page()

        """
        ratings = self._model.getRatings()
        for voto in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(voto))
            self._view._ddrating2.options.append(ft.dropdown.Option(voto))
        self._view.update_page()

        """
    # FINE PUNTO 1 ------------------------------------------------------

    # PUNTO 2,3 ----------------------------------------------------------
    def handleCreaGrafo(self, e):

        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        n = self._model.getNumNodes()
        m = self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi: "))
        top_5 = self._model.get_top_5_archi()
        for u, v, data in top_5:
            self._view.txt_result.controls.append(ft.Text(f"{u.Name} -> {v.Name} | Peso: {data['weight']}"))

        componenti, componente_max = self._model.getConnectedComponents()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(componenti)} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(componente_max)}:"))
        for c in componente_max:
            self._view.txt_result.controls.append(ft.Text(f"{c.Name}"))

        self._view.update_page()

    # FINE PUNTO 2,3 ------------------------------------------------------


    # PARTE 2 NON FATTA
    def handleCammino(self, e):

        bestPath = self._model.getBestPath()
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo trovato ({len(bestPath)} nodi):"))

        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.Name))

        self._view.update_page()