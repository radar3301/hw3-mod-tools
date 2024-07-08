import os
from tkinter import Tk, filedialog

def select_directory(prompt):
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=prompt)
    root.destroy()
    return folder_selected

config_vars = {
    'HW3TOOL_LOC': "Homeworld 3 Mod Tools and Editor",
    'HW3GAME_LOC': "Homeworld 3 Game",
}
config_paths = {
    'HW3TOOL_LOC': '"Epic Games\\Homeworld3ModToolsEditor"',
    'HW3GAME_LOC': '"SteamLibrary\\steamapps\\common\\Homeworld 3"',
}

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.hw3tool_loc = None
        self.hw3game_loc = None
        self.cached = {}

    def prompt_loc(self, var, reconfigure=False, optional=False):
        if optional:
            choice = input(f"Would you like to { 're' if reconfigure else '' }configure it now? [yes]/no: ").strip().lower()
            if choice == 'yes' or choice == '':
                return select_directory(f"Select the location of the {config_vars.get(var)} (e.g., {config_paths.get(var)})")
            else:
                return None
        else:
            return select_directory(f"Select the location of the {config_vars.get(var)} (e.g., {config_paths.get(var)})")

    def get_loc_var(self, var, value, optional = False):
        var_desc = config_vars.get(var)
        if value and not os.path.exists(value):
            print(f"The configured location for \"{var_desc}\" does not exist: {value}")
            value = self.prompt_loc(var, True, optional)
        elif not value:
            print(f"The location of \"{var_desc}\" has not been configured.")
            value = self.prompt_loc(var, False, optional)
        return value
    
    def load(self):
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key.strip()] = value.strip().strip('"')
            
            self.hw3tool_loc = self.get_loc_var('HW3TOOL_LOC', config.get('HW3TOOL_LOC'), True)
            self.hw3game_loc = self.get_loc_var('HW3GAME_LOC', config.get('HW3GAME_LOC'), True)
        else:
            self.hw3tool_loc = self.get_loc_var('HW3TOOL_LOC', None, True)
            self.hw3game_loc = self.get_loc_var('HW3GAME_LOC', None, True)

    def save(self):
        with open(self.config_path, 'w') as config_file:
            config_file.write(f'HW3TOOL_LOC="{self.hw3tool_loc}"\n')
            config_file.write(f'HW3GAME_LOC="{self.hw3game_loc}"\n')

    def get_tool_location(self):
        value = self.cached.get('hw3tool_loc')
        if not value:
            if not self.hw3tool_loc:
                self.hw3tool_loc = self.get_loc_var('HW3TOOL_LOC', None)
            value = self.cached['hw3tool_loc'] = self.hw3tool_loc
        return value

    def get_game_location(self):
        value = self.cached.get('hw3game_loc')
        if not value:
            if not self.hw3game_loc:
                self.hw3game_loc = self.get_loc_var('HW3GAME_LOC', None)
            value = self.cached['hw3game_loc'] = self.hw3game_loc;
        return value