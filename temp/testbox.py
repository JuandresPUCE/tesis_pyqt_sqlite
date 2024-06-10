from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget

class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Example")
        self.setGeometry(100, 100, 300, 200)

        # Setup central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create QComboBox
        self.registro_datos_box = QComboBox(self)
        layout.addWidget(self.registro_datos_box)

        # Example data
        registros = [
            {"nombre_data": "Registro 1", "id": 1},
            {"nombre_data": "Registro 2", "id": 2},
            {"nombre_data": "Registro 3", "id": 3}
        ]

        # Fill QComboBox with data
        self.mostrar_registros(registros)

    def mostrar_registros(self, registros):
        self.registro_datos_box.clear()
        self.registro_datos_box.addItem("Todos")
        if registros:
            for registro in registros:
                self.registro_datos_box.addItem(registro["nombre_data"], registro["id"])
        else:
            print("No se encontraron registros")

    def get_selected_id(self):
        return self.registro_datos_box.currentData()

if __name__ == "__main__":
    app = QApplication([])
    window = ExampleWindow()
    window.show()
    app.exec()
