import argparse
import os
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Konwersja danych między formatami JSON, YAML i XML.")
    parser.add_argument("input_file", help="Ścieżka do pliku wejściowego (.json, .yaml, .yml lub .xml)")
    parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego (.json, .yaml, .yml lub .xml)")
    args = parser.parse_args()

    # Walidacja rozszerzeń
    valid_extensions = {'.json', '.yaml', '.yml', '.xml'}
    input_ext = os.path.splitext(args.input_file)[1].lower()
    output_ext = os.path.splitext(args.output_file)[1].lower()

    if input_ext not in valid_extensions:
        parser.error(f"Plik wejściowy musi mieć jedno z rozszerzeń: {', '.join(valid_extensions)}")
    if output_ext not in valid_extensions:
        parser.error(f"Plik wyjściowy musi mieć jedno z rozszerzeń: {', '.join(valid_extensions)}")
    if not os.path.exists(args.input_file):
        parser.error(f"Plik wejściowy '{args.input_file}' nie istnieje")

    return args.input_file, args.output_file

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Nieprawidłowa składnia JSON w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.json'):
        data = read_json(input_file)
        print("Dane JSON wczytane:", data)
    else:
        print(f"Wejście: {input_file}, Wyjście: {output_file}")