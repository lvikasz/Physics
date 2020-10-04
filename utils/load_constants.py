import yaml

def load_constants():
    with open("../constants.yaml", 'r') as stream:
        try:
            yamlFile = yaml.safe_load(stream)

            g = yamlFile['g']
            dt = yamlFile['dt']
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    return (g, dt)