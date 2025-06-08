
import argparse
import os
import json
import yaml
from lxml import etree

def write_xml(data, file_path):
    try:
        tree = etree.ElementTree(data)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")
        
def read_xml(file_path):
    try:
        tree = etree.parse(file_path)
        return tree.getroot()  # Zwraca korzeń drzewa XML
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Nieprawidłowa składnia XML w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")

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
def write_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.json'):
        data = read_json(input_file)

        print("Dane JSON wczytane:", data)
    else:
        print(f"Wejście: {input_file}, Wyjście: {output_file}")

def read_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ValueError(f"Pusty lub nieprawidłowy plik YAML w {file_path}")
        return data
    except yaml.YAMLError as e:
        raise ValueError(f"Nieprawidłowa składnia YAML w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")
        
def write_yaml(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")
        
 if output_file.endswith('.json'):
            write_json(data, output_file)
            print(f"Przekonwertowano do {output_file}")

# Aktualizacja main
if __name__ == "__main__":
    input_file, output_file = parse_arguments()

    if input_file.endswith('.xml'):
        data = read_xml(input_file)
        if output_file.endswith('.xml'):
            write_xml(data, output_file)
            print(f"Przekonwertowano do {output_file}")pr

    if input_file.endswith('.xml'):
        data = read_xml(input_file)
        print("Dane XML wczytane:", etree.tostring(data, pretty_print=True).decode())

    if input_file.endswith(('.yaml', '.yml')):
        data = read_yaml(input_file)
        
        if output_file.endswith(('.yaml', '.yml')):
            write_yaml(data, output_file)
            print(f"Przekonwertowano do {output_file}")

        print("Dane YAML wczytane:", data)
