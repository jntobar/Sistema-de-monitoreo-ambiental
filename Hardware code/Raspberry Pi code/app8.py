from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import webview  # Usaremos pywebview para mostrar el dashboard
from kivy.core.window import Window

# Pantalla principal
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn_grafana = Button(text="Ver Dashboard de Grafana", size_hint=(1, 0.2))
        btn_grafana.bind(on_release=self.go_to_grafana)

        btn_datos = Button(text="Datos Curiosos", size_hint=(1, 0.2))
        btn_datos.bind(on_release=self.go_to_datos)

        layout.add_widget(btn_grafana)
        layout.add_widget(btn_datos)
        self.add_widget(layout)

    def go_to_grafana(self, instance):
        self.manager.current = "grafana"

    def go_to_datos(self, instance):
        self.manager.current = "datos"


# Pantalla de Grafana
class GrafanaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Botón para abrir el dashboard
        btn_open_dashboard = Button(text="Abrir Dashboard de Grafana", size_hint=(1, 0.2))
        btn_open_dashboard.bind(on_press=self.open_dashboard)

        # Botón para regresar al menú principal
        btn_volver = Button(text="Volver al Menú Principal", size_hint=(1, 0.2))
        btn_volver.bind(on_release=self.go_to_menu)

        layout.add_widget(btn_open_dashboard)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def open_dashboard(self, instance):
        screen_width = Window.width
        screen_height = Window.height

        # Crear la ventana del dashboard de Grafana en un iframe usando pywebview
        webview.create_window("Dashboard de Grafana", "http://localhost:3000/public-dashboards/0c7f514b3e0d4abc8903e93a6ed729e4", width=screen_width, height=screen_height)
        webview.start()

    def go_to_menu(self, instance):
        self.manager.current = "menu"


# Pantalla de Datos Curiosos
class DatosCuriososScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Texto de datos curiosos
        label = Label(text="¿Sabías que... las abejas tienen cinco ojos?", size_hint=(1, 0.8))
        btn_volver = Button(text="Volver al Menú Principal", size_hint=(1, 0.2))
        btn_volver.bind(on_release=self.go_to_menu)

        layout.add_widget(label)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def go_to_menu(self, instance):
        self.manager.current = "menu"


# Aplicación principal
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GrafanaScreen(name="grafana"))
        sm.add_widget(DatosCuriososScreen(name="datos"))
        return sm

    def on_start(self):
        # Asegúrate de que la ventana ocupe toda la pantalla
        Window.maximize()  # Maximiza la ventana para que ocupe toda la pantalla


if __name__ == "__main__":
    MyApp().run()
