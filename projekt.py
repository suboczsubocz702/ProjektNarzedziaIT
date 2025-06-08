import argparse
import os

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

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    print(f"Wejście: {input_file}, Wyjście: {output_file}")
