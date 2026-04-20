import json
import pystache
import os


def generate_UnifiedRaceState():
    current_directory = os.getcwd()
    
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)

    with open("UnifiedRaceState.mustache", "r") as f:
        template = f.read()

    with open("UnifiedRaceState.json", "r") as f:
        data = json.load(f)

    rendered = pystache.render(template, data)

    with open("UnifiedRaceState.py", "w") as f:
        f.write(rendered)

    os.chdir(current_directory)

if __name__ == "__main__":
    generate_UnifiedRaceState()
