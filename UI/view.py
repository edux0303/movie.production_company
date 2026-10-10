import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Gruppo Case di Produzione"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._ddAnno = None
        self._txtM = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None
        self._ddCasa = None
        self._txtN = None
        self._btnTrovaGruppo = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Gruppo Case di Produzione", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._ddAnno = ft.Dropdown(label="Anno", width=150)
        self._txtM = ft.TextField(label="Min film M", width=150, value="4")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo)
        row1 = ft.Row([self._ddAnno, self._txtM, self._btnCreaGrafo, self._btnStampaInfo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # PUNTO 2
        self._ddCasa = ft.Dropdown(label="Casa di partenza", width=350)
        self._txtN = ft.TextField(label="N case", width=150)
        self._btnTrovaGruppo = ft.ElevatedButton(text="Trova Gruppo",
                                                 on_click=self._controller.handleTrovaGruppo)
        row2 = ft.Row([self._ddCasa, self._txtN, self._btnTrovaGruppo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        # gli anni si possono caricare subito, le case solo dopo "Crea Grafo"
        self._controller.fillDDAnni()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()