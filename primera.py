from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QStackedWidget, QVBoxLayout, QWidget
import sys
from segunda import MiVentana2  # Importa la segunda ventana

class MiVentana(QDialog):
    def __init__(self, parent=None):
        super(MiVentana, self).__init__(parent)
        
        self.stacked_widget = QStackedWidget()  # Crea un nuevo QStackedWidget
        self.boton = QPushButton('Abrir segunda ventana', self)
        self.boton.clicked.connect(self.abrir_segunda_ventana)  # Conecta el botón con la función abrir_segunda_ventana
        self.ventana2 = MiVentana2(self)  # Crea una nueva instancia de la segunda ventana

        self.stacked_widget.addWidget(QWidget())  # Añade un widget vacío al QStackedWidget
        self.stacked_widget.addWidget(self.ventana2)  # Añade la segunda ventana al QStackedWidget

        layout = QVBoxLayout()  # Crea un nuevo layout vertical
        layout.addWidget(self.boton)  # Añade el botón al layout
        layout.addWidget(self.stacked_widget)  # Añade el QStackedWidget al layout
        self.setLayout(layout)  # Establece el layout de la ventana

        self.show()

    def abrir_segunda_ventana(self):
        self.stacked_widget.setCurrentWidget(self.ventana2)  # Muestra la segunda ventana en el QStackedWidget

if __name__=="__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())