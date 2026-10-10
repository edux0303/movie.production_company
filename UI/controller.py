import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnni(self):          # punto 1a: riempie il dropdown degli anni
        for a in self._model.getAnni():
            self._view._ddAnno.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        anno = self._view._ddAnno.value
        if anno is None:
            self._errore("Selezionare un anno!")
            return
        try:
            minimo = int(self._view._txtM.value)
        except ValueError:
            self._errore("M deve essere un intero!")
            return
        if minimo < 1:
            self._errore("M deve essere almeno 1!")
            return

        self._model.buildGraph(int(anno), minimo)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato per l'anno {anno}!"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddCasa.options.clear()
        self._view._ddCasa.value = None
        for c in self._model.getNodes():
            self._view._ddCasa.options.append(ft.dropdown.Option(key=c.nome, text=c.nome))
        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        casa, peso = self._model.getCasaSommaMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Casa con somma dei pesi massima: {casa} ({peso})"))

        self._view.txt_result.controls.append(ft.Text("I 5 archi di peso maggiore:"))
        for nome1, nome2, p in self._model.getTop5():
            self._view.txt_result.controls.append(ft.Text(f"{nome1} - {nome2}: {p}"))

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi di peso 1: {self._model.getPesiUno()}"))
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleTrovaGruppo(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        nomeCasa = self._view._ddCasa.value
        if nomeCasa is None:
            self._errore("Selezionare una casa di partenza!")
            return
        partenza = self._model.idMap[nomeCasa]

        try:
            n = int(self._view._txtN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un intero!")
            return
        if n < 1:
            self._errore("N deve essere almeno 1!")
            return
        if n > self._model.getNumNodi():
            self._errore(f"N non può superare il numero di case ({self._model.getNumNodi()})!")
            return

        gruppo, voti = self._model.getGruppo(partenza, n)
        if len(gruppo) == 0:
            self._errore(f"Nessun gruppo valido di {n} case partendo da {partenza}")
            return

        self._view.txt_result.controls.append(ft.Text(f"Gruppo trovato partendo da {partenza}:"))
        for c in sorted(gruppo, key=lambda x: x.nome):
            self._view.txt_result.controls.append(
                ft.Text(f"{c.nome} - film: {c.numFilm}, voti: {c.voti}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di case: {len(gruppo)}"))
        self._view.txt_result.controls.append(ft.Text(f"Voti complessivi: {voti}"))
        self._view.update_page()