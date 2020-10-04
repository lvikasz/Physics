import yaml

with open("constants.yaml", "r") as stream:
    print(yaml.safe_load(stream))
