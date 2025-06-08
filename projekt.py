from lxml import etree

def read_xml(file_path):
    try:
        tree = etree.parse(file_path)
        return tree.getroot()  # Zwraca korzeń drzewa XML
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Nieprawidłowa składnia XML w {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Błąd podczas wczytywania {file_path}: {e}")

# Aktualizacja main
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.xml'):
        data = read_xml(input_file)
        print("Dane XML wczytane:", etree.tostring(data, pretty_print=True).decode())
