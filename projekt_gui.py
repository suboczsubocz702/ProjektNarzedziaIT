from PyQt5.QtCore import QThread, pyqtSignal

class ConverterThread(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
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

            self.result.emit(f"Konwersja zakończona: {self.output_file}")
        except Exception as e:
            self.error.emit(f"Błąd: {e}")

# Aktualizacja ConverterWindow
class ConverterWindow(QMainWindow):
    # ... (poprzedni kod aż do convert_files)
    def convert_files(self):
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
        self.status_label.setText(message)

    def on_conversion_error(self, message):
        self.status_label.setText(message)

    def on_conversion_finished(self):
        self.convert_button.setEnabled(True)
