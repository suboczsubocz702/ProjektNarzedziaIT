def write_yaml(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
    except Exception as e:
        raise IOError(f"Błąd podczas zapisu do {file_path}: {e}")

# Aktualizacja main
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith(('.yaml', '.yml')):
        data = read_yaml(input_file)
        if output_file.endswith(('.yaml', '.yml')):
            write_yaml(data, output_file)
            print(f"Przekonwertowano do {output_file}")
