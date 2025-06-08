def write_xml(data, file_path):
    try:
        tree = etree.ElementTree(data)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

# Aktualizacja main
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.xml'):
        data = read_xml(input_file)
        if output_file.endswith('.xml'):
            write_xml(data, output_file)
            print(f"Przekonwertowano do {output_file}")pr
