import sys
from PyQt6.QtWidgets import QApplication
from test_RC_panel_analizar_datos_controlador import PanelDataAnalisis

def main():
    app = QApplication(sys.argv)
    mainWindow = PanelDataAnalisis()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()