import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from project import read_json, write_json, read_yaml, write_yaml, read_xml, write_xml, xml_to_dict, dict_to_xml

class ConverterThread(QThread):
    """Wątek do asynchronicznego wczytywania i zapisywania plików."""
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        try:
            # Wczytywanie danych
            input_ext = self.input_file.lower().rsplit('.', 1)[1]
            if input_ext == 'json':
                data = read_json(self.input_file)
            elif input_ext in ('yaml', 'yml'):
                data = read_yaml(self.input_file)
            elif input_ext == 'xml':
                xml_data = read_xml(self.input_file)
                data = xml_to_dict(xml_data)
            else:
                raise ValueError(f"Nieobsługiwany format pliku wejściowego: {input_ext}")

            # Zapis danych
            output_ext = self.output_file.lower().rsplit('.', 1)[1]
            if output_ext == 'json':
                write_json(data, self.output_file)
            elif output_ext in ('yaml', 'yml'):
                write_yaml(data, self.output_file)
            elif output_ext == 'xml':
                xml_data = dict_to_xml(data)
                write_xml(xml_data, self.output_file)
            else:
                raise ValueError(f"Nieobsługiwany format pliku wyjściowego: {output_ext}")

            self.result.emit(f"Konwersja zakończona pomyślnie: {self.output_file}")
        except Exception as e:
            self.error.emit(f"Błąd: {str(e)}")

class ConverterWindow(QMainWindow):
    """Główne okno aplikacji GUI do konwersji danych."""
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
        """Otwiera okno dialogowe do wyboru pliku wejściowego."""
        file, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejściowy", "", "Pliki danych (*.json *.yaml *.yml *.xml)")
        if file:
            self.input_file = file
            self.status_label.setText(f"Wejście: {file}")

    def select_output(self):
        """Otwiera okno dialogowe do wyboru pliku wyjściowego."""
        file, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wyjściowy", "", "Pliki danych (*.json *.yaml *.yml *.xml)")
        if file:
            self.output_file = file
            self.status_label.setText(f"Wyjście: {file}")

    def convert_files(self):
        """Uruchamia asynchroniczną konwersję plików."""
        if not self.input_file or not self.output_file:
            self.status_label.setText("Wybierz oba pliki: wejściowy i wyjściowy.")
            return

        self.convert_button.setEnabled(False)
        self.status_label.setText("Konwertowanie...")
        self.thread = ConverterThread(self.input_file, self.output_file)
        self.thread.result.connect(self.on_conversion_success)
        self.thread.error.connect(self.on_conversion_error)
        self.thread.finished.connect(self.on_conversion_finished)
        self.thread.start()

    def on_conversion_success(self, message):
        """Obsługuje sukces konwersji."""
        self.status_label.setText(message)

    def on_conversion_error(self, message):
        """Obsługuje błędy konwersji."""
        self.status_label.setText(message)

    def on_conversion_finished(self):
        """Przywraca aktywność przycisku po zakończeniu konwersji."""
        self.convert_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())
