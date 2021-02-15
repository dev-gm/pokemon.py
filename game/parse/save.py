"""The module that parses the json data to be passed
into the program, using mainly the Save class"""

import json
import os

class Save:
    """A class that processes (vars, operations) and holds all of the
    data from a data json file that is given, passed into Game folder"""

    def __init__(self, name: str = json.load(open("./saves/save.json", 'r')).get("save"), folder: str = "./saves/", filename: str = "data.json"):
        """Gets data json file and gets processed reusable
        components and maps from it"""
        self.name = name
        self.folder = folder
        self.save_folder = os.path.join(self.folder, self.name)
        self.path = os.path.join(self.folder, self.name, filename)
        self.raw_reusables = {}
        with open(self.path, 'r') as file:
            self.raw_data = json.load(file)
        self.data = self.raw_data
        for raw_reusable in self.data.pop("reusable").values():
            self.raw_reusables.update(raw_reusable)
        self.reusables = self.process_reusables(self.raw_reusables)
        self.data = self.process_component(self.data)

    def process_component(self, component):
        """Recursive method that goes through a component (like json data[maps])
        and all of its children to see any references to reusable components"""
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
        """Goes through raw reusables from json data and puts individual
        raw components through Save.process_reusable()"""
        reusables = {}
        for name, reusable in raw_reusables.items():
            if name not in reusables.keys():
                reusables[name] = self.process_reusable(reusable, reusables, raw_reusables)
        return reusables

    def process_reusable(self, reusable, reusables: dict, raw_reusables: dict):
        """Processes references to other reusable components in a reusable
        component by using recursion to process all sub-items"""
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
                raw_reusable = raw_reusables.get(name)
                if raw_reusable:
                    if name not in reusables.keys():
                        reusables[name] = self.process_reusable(raw_reusable, reusables, raw_reusables)
                    return reusables.get(name)
        return reusable

    def is_reusable(self, text: str):
        """Checks if text starts with 'reuse ', which would mean
        that it is referencing a reusable component"""
        if text[:6] == "reuse ":
            return True
        return False

    def get_player_info(self):
        """Returns current player info including current map and pos"""
        return self.data.get("player").get("current")

    def get_data(self):
        """Returns processed data without reusable or vars"""
        return self.data

    def update_player(self, new_current: dict):
        """Updates current player info such as map and pos of player"""
        self.raw_data["player"]["current"] = new_current
        self.update_file()
        self.data["player"]["current"] = self.process_component(new_current)

    def update_file(self):
        """Writes updated (current pos/map) raw data to json output file"""
        with open(self.path, 'w') as file:
            json.dump(self.raw_data, file)
