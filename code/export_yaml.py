import yaml
import os


def save_yaml(data, path="../data/resume.yaml"):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    yaml_data = {"produits": data}

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

    print("YAML créé :", path)