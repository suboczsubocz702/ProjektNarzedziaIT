import argparse
import os
import json
import yaml
from lxml import etree

def parse_arguments():
    """Parsuje argumenty wiersza poleceń dla pliku wejściowego i wyjściowego."""
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
    """Wczytuje dane z pliku JSON i zwraca je jako obiekt Pythona."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Nieprawidłowa składnia JSON w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")

def write_json(data, file_path):
    """Zapisuje dane do pliku JSON."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

def read_yaml(file_path):
    """Wczytuje dane z pliku YAML i zwraca je jako obiekt Pythona."""
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
    """Zapisuje dane do pliku YAML."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

def read_xml(file_path):
    """Wczytuje dane z pliku XML i zwraca korzeń drzewa XML."""
    try:
        tree = etree.parse(file_path)
        return tree.getroot()
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Nieprawidłowa składnia XML w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")

def write_xml(data, file_path):
    """Zapisuje dane XML do pliku."""
    try:
        tree = etree.ElementTree(data)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

def xml_to_dict(element):
    """Konwertuje element XML na słownik Pythona."""
    result = {}
    if element.text and element.text.strip():
        result['text'] = element.text.strip()
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    for key, value in element.attrib.items():
        result[f"@{key}"] = value
    return result

def dict_to_xml(data, root_tag="root"):
    """Konwertuje słownik Pythona na element XML."""
    def _to_xml(data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith('@'):
                    parent.set(key[1:], value)
                elif key == 'text':
                    parent.text = value
                elif isinstance(value, list):
                    for item in value:
                        child = etree.SubElement(parent, key)
                        _to_xml(item, child)
                else:
                    child = etree.SubElement(parent, key)
                    _to_xml(value, child)
        elif isinstance(data, (str, int, float, bool)):
            parent.text = str(data)
        elif data is None:
            pass
        else:
            raise ValueError(f"Nieobsługiwany typ danych: {type(data)}")

    root = etree.Element(root_tag)
    _to_xml(data, root)
    return root

if __name__ == "__main__":
    try:
        input_file, output_file = parse_arguments()
        input_ext = os.path.splitext(input_file)[1].lower()
        output_ext = os.path.splitext(output_file)[1].lower()

        # Wczytywanie danych
        if input_ext == '.json':
            data = read_json(input_file)
        elif input_ext in ('.yaml', '.yml'):
            data = read_yaml(input_file)
        elif input_ext == '.xml':
            xml_data = read_xml(input_file)
            data = xml_to_dict(xml_data)
        else:
            raise ValueError(f"Nieobsługiwany format pliku wejściowego: {input_ext}")

        # Zapis danych
        if output_ext == '.json':
            write_json(data, output_file)
        elif output_ext in ('.yaml', '.yml'):
            write_yaml(data, output_file)
        elif output_ext == '.xml':
            xml_data = dict_to_xml(data)
            write_xml(xml_data, output_file)
        else:
            raise ValueError(f"Nieobsługiwany format pliku wyjściowego: {output_ext}")

        print(f"Konwersja zakończona pomyślnie: {input_file} -> {output_file}")

    except Exception as e:
        print(f"Błąd: {e}")
        exit(1)
