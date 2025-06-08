def write_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

# Aktualizacja main dla konwersji
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.json'):
        data = read_json(input_file)
        if output_file.endswith('.json'):
            write_json(data, output_file)
            print(f"Przekonwertowano do {output_file}")
