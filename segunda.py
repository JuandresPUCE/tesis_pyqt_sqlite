from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
import sys

class MiVentana2(QDialog):
    def __init__(self, parent=None):
        super(MiVentana2, self).__init__(parent)
        
        # Crea un nuevo botón
        self.boton = QPushButton('Mi Botón', self)
        self.boton.move(50, 50)  # Mueve el botón a la posición (50, 50)

        self.show()

if __name__=="__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana2()
    sys.exit(app.exec_())