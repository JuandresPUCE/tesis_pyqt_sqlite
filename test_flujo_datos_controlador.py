import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import *
from modelos import *
from repositorios import *
import logging

#importe ui de la ventana principal
from flujo_datos_vista import Ui_MainWindow

# metodos comunes
from servicios import *

class FlujoDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlujoDatos()
    window.show()
    sys.exit(app.exec())