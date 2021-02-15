import json
import os


class Save:
    def __init__(self, name: str = json.load(open("./saves/save.json", 'r')).get("save"), folder: str = "./saves/", filename: str = "data.json"):
        self.name = name
        self.folder = folder
        self.raw_reusables = {}
        with open(os.path.join(self.folder, name, filename), 'r') as file:
            self.data = json.load(file)
        for raw_reusable in self.data.get("reusable").values():
            self.raw_reusables.update(raw_reusable)
        self.reusables = self.process_reusables(self.raw_reusables)
        self.maps = self.process_component(self.data.get("maps"))

    def process_component(self, component):
        if isinstance(component, dict):
            return {name: self.process_component(sub_component)
                    for name, sub_component in component.items()}
        elif isinstance(component, list):
            return [self.process_component(sub_component)
                    for sub_component in component]
        elif isinstance(component, str):
            if self.is_reusable(component):
                return self.reusables.get(component[6:])
        return component

    def process_reusables(self, raw_reusables: dict):
        reusables = {}
        for name, reusable in raw_reusables.items():
            if name not in reusables.keys():
                reusables[name] = self.process_reusable(reusable, reusables, raw_reusables)
        return reusables

    def process_reusable(self, reusable, reusables: dict, raw_reusables: dict):
        if reusable in reusables.values():
            return reusable
        elif isinstance(reusable, dict):
            return {name: self.process_reusable(sub_reusable, reusables, raw_reusables)
                    for name, sub_reusable in reusable.items()}
        elif isinstance(reusable, list):
            return [self.process_reusable(sub_reusable, reusables, raw_reusables)
                    for sub_reusable in reusable]
        elif isinstance(reusable, str):
            if self.is_reusable(reusable):
                name = reusable[6:]
                print(name)
                raw_reusable = raw_reusables.get(name)
                if raw_reusable:
                    if name not in reusables.keys():
                        reusables[name] = self.process_reusable(raw_reusable, reusables, raw_reusables)
                    return reusables.get(name)
        return reusable

    def is_reusable(self, text: str):
        if text[:6] == "reuse ":
            return True
        return False
