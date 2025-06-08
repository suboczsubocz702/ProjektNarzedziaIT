import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from project import read_json, write_json, read_yaml, write_yaml, read_xml, write_xml

class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter Danych")
        self.setGeometry(100, 100, 400, 200)

        # Układ
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Widgety
        self.status_label = QLabel("Wybierz pliki wejściowy i wyjściowy.")
        self.input_button = QPushButton("Wybierz plik wejściowy")
        self.output_button = QPushButton("Wybierz plik wyjściowy")
        self.convert_button = QPushButton("Konwertuj")

        layout.addWidget(self.status_label)
        layout.addWidget(self.input_button)
        layout.addWidget(self.output_button)
        layout.addWidget(self.convert_button)

        # Połączenie przycisków
        self.input_button.clicked.connect(self.select_input)
        self.output_button.clicked.connect(self.select_output)
        self.convert_button.clicked.connect(self.convert_files)

        self.input_file = None
        self.output_file = None

    def select_input(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejściowy", "", "Pliki danych (*.json *.yaml *.yml *.xml)")
        if file:
            self.input_file = file
            self.status_label.setText(f"Wejście: {file}")

    def select_output(self):
        file, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wyjściowy", "", "Pliki danych (*.json *.yaml *.yml *.xml)")
        if file:
            self.output_file = file
            self.status_label.setText(f"Wyjście: {file}")

    def convert_files(self):
        if not self.input_file or not self.output_file:
            self.status_label.setText("Wybierz oba pliki: wejściowy i wyjściowy.")
            return

        try:
            # Wczytanie danych
            if self.input_file.endswith('.json'):
                data = read_json(self.input_file)
            elif self.input_file.endswith(('.yaml', '.yml')):
                data = read_yaml(self.input_file)
            elif self.input_file.endswith('.xml'):
                data = read_xml(self.input_file)

            # Zapis danych
            if self.output_file.endswith('.json'):
                write_json(data, self.output_file)
            elif self.output_file.endswith(('.yaml', '.yml')):
                write_yaml(data, self.output_file)
            elif self.output_file.endswith('.xml'):
                write_xml(data, self.output_file)

            self.status_label.setText(f"Konwersja zakończona: {self.output_file}")
        except Exception as e:
            self.status_label.setText(f"Błąd: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())
