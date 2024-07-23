from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataFrame a QTableWidget")
        self.setGeometry(100, 100, 600, 400)

        # Suponiendo que tienes un DataFrame llamado df
        df = pd.DataFrame({
            'Columna1': [1, 2, 3, 4],
            'Columna2': ['A', 'B', 'C', 'D']
        })

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.convertir_df_a_qtablewidget(df)

    def convertir_df_a_qtablewidget(self, df):
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for index, row in df.iterrows():
            for col_index, value in enumerate(row):
                self.tableWidget.setItem(index, col_index, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()