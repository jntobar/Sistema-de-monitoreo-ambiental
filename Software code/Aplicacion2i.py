from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import csv
Window.clearcolor = (1,1, 1, 1)  # Cambia el fondo de la ventana a un color (R, G, B, Alpha)


# Pantalla principal
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn_grafana = Button(text="Ver Dashboard de Grafana", size_hint=(1, 0.2))
        btn_grafana.bind(on_release=self.go_to_grafana)

        btn_datos = Button(text="Datos Curiosos", size_hint=(1, 0.2))
        btn_datos.bind(on_release=self.go_to_datos)
        
        btn_satisfaccion = Button(text="Satisfacción del Cliente", size_hint=(1, 0.2))
        btn_satisfaccion.bind(on_release=self.go_to_satisfaccion)

        layout.add_widget(btn_grafana)
        layout.add_widget(btn_datos)
        layout.add_widget(btn_satisfaccion)
        self.add_widget(layout)

    def go_to_grafana(self, instance):
        self.manager.current = "grafana"

    def go_to_datos(self, instance):
        self.manager.current = "datos"
        
    def go_to_satisfaccion(self, instance):
        self.manager.current = "satisfaccion"

# Pantalla de Grafana
class GrafanaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Botón para abrir el dashboard
        btn_open_dashboard = Button(text="Abrir Dashboard de Grafana", size_hint=(1, 0.2))
        btn_open_dashboard.bind(on_press=self.open_dashboard)

        # Botón para regresar al menú principal
        btn_volver = Button(text="Volver al Menú Principal", size_hint=(1, 0.1))
        btn_volver.bind(on_release=self.go_to_menu)

        layout.add_widget(btn_open_dashboard)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def open_dashboard(self, instance):
        screen_width = Window.width
        screen_height = Window.height

        # Crear la ventana del dashboard de Grafana en un iframe usando pywebview
        import webview
        webview.create_window("Dashboard de Grafana", "http://localhost:3000/public-dashboards/452c06edd8db40f79bf3d34d2f02ef1d", width=screen_width, height=screen_height)
        webview.start()

    def go_to_menu(self, instance):
        self.manager.current = "menu"


# Pantalla de Datos Curiosos
class DatosCuriososScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Lista de preguntas y respuestas
        preguntas_respuestas = [
            ("¿Sabías que la calidad del aire puede influir en tu salud mental?", "La exposición a niveles altos de contaminación puede aumentar el riesgo de ansiedad y depresión."),
            ("¿Sabías que el nivel ideal de humedad está entre 40% y 60%?", "El aire demasiado seco o húmedo puede afectar tu bienestar, especialmente la piel y las vías respiratorias."),
            ("¿Sabías que la temperatura ideal para el confort humano está entre 18°C y 22°C?", "Temperaturas extremas pueden causar estrés térmico en el cuerpo."),
            ("¿Sabías que cuando la presión atmosférica disminuye, a menudo se asocia con mal tiempo?", "La disminución de presión se asocia con la llegada de tormentas o lluvias."),
            ("¿Sabías que el dióxido de carbono (CO2) es un gas que exhalamos al respirar?", "Niveles altos de CO2 pueden generar somnolencia y dificultades para concentrarse."),
            ("¿Sabías que las partículas finas en el aire (PM2.5) pueden afectar tus pulmones?", "Estas partículas son tan pequeñas que pueden penetrar profundamente en los pulmones y causar problemas respiratorios."),
            ("¿Sabías que la lluvia ayuda a limpiar el aire?", "Durante una tormenta, los contaminantes en el aire se disuelven y caen al suelo."),
            ("¿Sabías que el ruido constante puede afectar tu salud?", "Exposición a ruidos fuertes aumenta el riesgo de estrés, alteraciones en el sueño y problemas cardiovasculares."),
        ]

        # Crear un ScreenManager para manejar las pantallas de cada pregunta
        sm = ScreenManager()

        self.questions_screens = []  # Guardar las pantallas de preguntas

        for i, (pregunta, respuesta) in enumerate(preguntas_respuestas):
            question_screen = QuestionScreen(pregunta, respuesta, name=f"pregunta_{i}")
            sm.add_widget(question_screen)
            self.questions_screens.append(question_screen)  # Guardar la referencia de cada pantalla


        # Botón para regresar al menú principal
        btn_volver = Button(text="Volver al Menú Principal", size_hint=(1, 0.1), font_size=24)
        btn_volver.bind(on_release=self.go_to_menu)

        # Agregar el ScreenManager y el botón al layout
        layout.add_widget(sm)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def go_to_menu(self, instance):
        self.manager.current = "menu"

        # Reiniciar las respuestas a su estado original
        self.reset_all_answers()
        
    def reset_all_answers(self):
        # Reiniciar las respuestas de todas las pantallas de preguntas
        for question_screen in self.questions_screens:
            question_screen.reset_answer()


# Pantalla de cada pregunta
class QuestionScreen(Screen):
    def __init__(self, pregunta, respuesta, **kwargs):
        super().__init__(**kwargs)
        self.pregunta = pregunta
        self.respuesta = respuesta

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Cuadro grande con la pregunta
        question_button = Button(text=self.pregunta, size_hint=(1, 0.9), background_normal="", background_color=(0.5, 0.5, 0.9, 1),font_size=20)
        question_button.bind(on_press=self.show_answer)

        # Label para la respuesta, inicialmente oculta
        self.answer_label = Label(text=self.respuesta, size_hint=(1, 0.9), opacity=0,color=(0, 0, 0, 1),font_size=17.5)

        # Agregar la pregunta y la respuesta al layout
        layout.add_widget(question_button)
        layout.add_widget(self.answer_label)

        # Botón para ir a la siguiente pregunta
        btn_siguiente = Button(text="Siguiente", size_hint=(1, 0.2),font_size=24)
        btn_siguiente.bind(on_release=self.next_question)
        layout.add_widget(btn_siguiente)

        self.add_widget(layout)

    def show_answer(self, instance):
        # Mostrar la respuesta
        self.answer_label.opacity = 1

    def next_question(self, instance):
        # Obtener el índice actual y calcular el siguiente
        current_index = int(self.name.split('_')[-1])
        next_index = current_index + 1

        # Verificar si existe una pantalla siguiente
        next_screen_name = f"pregunta_{next_index}"
        if next_screen_name in self.manager.screen_names:
            self.manager.current = next_screen_name
        else:
            # Si no hay más preguntas, redirigir al menú o reiniciar las preguntas
            self.manager.current = "pregunta_0"  # Opcional: Redirigir al inicio de las preguntas

    def reset_answer(self):
        # Reiniciar la visibilidad de la respuesta a su estado original
        self.answer_label.opacity = 0    


# Pantalla satisfaccion cliente
class SatisfaccionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=30)

        # Label de introducción
        label = Label(text="¿Cómo calificarías tu satisfacción con respecto al Sistema de Monitoreo?", size_hint=(1, 0.2),color=(0, 0, 0, 1), font_size=25)
        layout.add_widget(label)

        # Crear un layout horizontal para los botones de satisfacción
        caritas_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.3))

        # Crear botones con texto y colores para los niveles de satisfacción
        self.satisfaccion = []
        self.contadores = [0, 0, 0, 0, 0]  # Contadores para cada nivel de satisfacción
        niveles = ["Muy Satisfecho", "Satisfecho", "Indiferente", "Insatisfecho", "Muy Insatisfecho"]
        colores = ["#008000", "#9ACD32", "#FFD700", "#FF4500", "#FF0000"]  # Verde, Verde claro, Amarillo, Naranja, Rojo
        
        for i in range(5):
            boton = Button(
                text=niveles[i], 
                background_color=self.hex_to_rgb(colores[i]), 
                size_hint=(2, 1),  # Para que los botones se ajusten en el alto, pero el ancho es fijo
                font_size=23
            )
            boton.bind(on_press=self.set_satisfaccion)
            self.satisfaccion.append(boton)
            caritas_layout.add_widget(boton)

        layout.add_widget(caritas_layout)

        # Botón para volver al menú principal
        btn_volver = Button(text="Volver al Menú Principal", size_hint=(1, 0.1), font_size=24)
        btn_volver.bind(on_release=self.go_to_menu)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def on_enter(self):
        """Método que se llama cuando la pantalla es cargada o recargada"""
        self.reiniciar_boton()

    def reiniciar_boton(self):
    	"""Restablecer los botones a su estado original (sin ser presionados)"""
    	for i, boton in enumerate(self.satisfaccion):
        	# Solo restaurar el color de los botones si no han sido seleccionados
        	if boton.background_color != (1, 1, 1, 1):  # Si el botón no está resaltado
            		boton.background_normal = 'button.png'  # Restaurar imagen de fondo predeterminada
            		boton.background_color = self.hex_to_rgb(["#008000", "#9ACD32", "#FFD700", "#FF4500", "#FF0000"][i])  # Restaurar su color original según el índice
	

    def set_satisfaccion(self, instance):
        # Resaltar el botón seleccionado y cambiar su estilo
        index = self.satisfaccion.index(instance)
        for i, boton in enumerate(self.satisfaccion):
            if i == index:
                boton.background_normal = ''
                boton.background_color = (1, 1, 1, 1)  # Resaltar
            else:
                boton.background_normal = 'button.png'

        # Incrementar el contador para el nivel de satisfacción seleccionado
        self.contadores[index] += 1
        print(f"Nivel de satisfacción seleccionado: {instance.text}")
        print(f"Contadores actuales: {self.contadores}")
        
        # Guardar los contadores en el archivo CSV
        self.guardar_datos()

        # Reiniciar botones después de marcar
        self.reiniciar_boton()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def guardar_datos(self):
        """Guardar los datos de satisfacción en un archivo CSV"""
        archivo_csv = "satisfaccion.csv"  # El archivo CSV se guarda en el directorio actual del script
        
        # Escribir los datos en el archivo CSV
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Muy Satisfecho", "Satisfecho", "Indiferente", "Insatisfecho", "Muy Insatisfecho"])
            writer.writerow(self.contadores)
        print(f"Datos guardados en {archivo_csv}")

    def go_to_menu(self, instance):
        self.manager.current = "menu"



# Administrador de pantallas
class MyApp(App):
    def build(self):
        # Ajustar tamaño de la ventana al tamaño de la pantalla completa
        Window.size = (Window.width, Window.height)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GrafanaScreen(name="grafana"))
        sm.add_widget(DatosCuriososScreen(name="datos"))
        sm.add_widget(SatisfaccionScreen(name="satisfaccion"))
        return sm
    def on_start(self):
        # Asegúrate de que la ventana ocupe toda la pantalla
        Window.maximize()  # Maximiza la ventana para que ocupe toda la pantalla

if __name__ == '__main__':
    MyApp().run()
