import sys
from PyQt6.QtWidgets import QApplication
from procesar_datos_controlador import PanelDataAnalisis

def main():
    app = QApplication(sys.argv)
    mainWindow = PanelDataAnalisis()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()