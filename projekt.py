import yaml

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

# Aktualizacja main
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith(('.yaml', '.yml')):
        data = read_yaml(input_file)
        print("Dane YAML wczytane:", data)
