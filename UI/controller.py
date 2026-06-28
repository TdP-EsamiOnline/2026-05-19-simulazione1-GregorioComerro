import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for genre in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=str(genre.GenreId), text=genre.Name)
            )

    def handleCreaGrafo(self, e):
        if self._view._ddGenre.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona un genere"))
            self._view.update_page()
            return

        idGenre = self._view._ddGenre.value
        self._model.buildGraph(idGenre)
        top5 = self._model.getTop5Archi()
        artist, influenza = self._model.getArtistMaxInfluence()

        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. Il grafo contiene {Nnodes} nodi e {Nedges} archi"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {artist}, con influenza:{influenza}"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]}: {arco[2]["weight"]}"))

        self._view.update_page()

        


    def handleCammino(self,e):
        pass

