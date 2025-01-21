"""Noah's improved Forza Track Selector"""
import random
import customtkinter
import options
import utilities

class App(customtkinter.CTk):
    """Main application class"""
    # pylint: disable=too-many-instance-attributes
    # To be reviewed further
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Forza Track Selector")
        self.geometry("800x480")
        # Init variables
        self.file = 'Settings.ini'
        # Define the GUI
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10)
        self.frame.grid_columnconfigure(0, weight=1, minsize=400)
        self.frame.grid_columnconfigure(1, weight=0, minsize=200)
        self.frame.grid_rowconfigure(0, weight=1)
        self.options_frame = customtkinter.CTkFrame(self.frame, width=300)
        self.options_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.stats_frame = customtkinter.CTkFrame(self.frame, width=200)
        self.stats_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.buttons_frame = customtkinter.CTkFrame(self.frame)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.random_button = customtkinter.CTkButton(self.buttons_frame,
                                                     text="Random Track",
                                                     command=lambda: [self.roll.track(),
                                                                      self.roll.weather(),
                                                                      self.roll.time(),
                                                                      self.history.update_total()])
        self.random_button.grid(row=0, column=0, padx=10, pady=10)
        self.reset_button = customtkinter.CTkButton(self.buttons_frame,
                                                    text="Reset",
                                                    command=lambda: [self.history.reset()])
        self.reset_button.grid(row=1, column=0, padx=10, pady=10)
        self.location_label = customtkinter.CTkLabel(self.options_frame, text="Location: ")
        self.location_label.grid(row=2, column=0, padx=10, pady=10)
        self.location_text = customtkinter.CTkLabel(self.options_frame, text="")
        self.location_text.grid(row=2, column=1, padx=10, pady=10)
        self.layout_label = customtkinter.CTkLabel(self.options_frame, text="Layout: ")
        self.layout_label.grid(row=3, column=0, padx=10, pady=10)
        self.layout_text = customtkinter.CTkLabel(self.options_frame, text="")
        self.layout_text.grid(row=3, column=1, padx=10, pady=10)
        self.weather_label = customtkinter.CTkLabel(self.options_frame, text="Weather: ")
        self.weather_label.grid(row=4, column=0, padx=10, pady=10)
        self.weather_text = customtkinter.CTkLabel(self.options_frame, text="")
        self.weather_text.grid(row=4, column=1, padx=10, pady=10)
        self.time_label = customtkinter.CTkLabel(self.options_frame, text="Time: ")
        self.time_label.grid(row=5, column=0, padx=10, pady=10)
        self.time_text = customtkinter.CTkLabel(self.options_frame, text="")
        self.time_text.grid(row=5, column=1, padx=10, pady=10)
        self.total_races_label = customtkinter.CTkLabel(self.stats_frame, text="Total Races:")
        self.total_races_label.grid(row=1, column=0, padx=10, pady=10)
        self.total_races_text = customtkinter.CTkLabel(self.stats_frame, text="0")
        self.total_races_text.grid(row=1, column=1, padx=10, pady=10)

        # Init classes
        self.logs = Logs(self)
        self.settings = Settings(self)
        self.history = History(self)
        self.roll = Roll(self)
        self.settings.validate()

class Logs:
    """Class to manage logs"""
    def __init__(self, app):
        self.app = app
        self.logs = utilities.Logs(app_name="Forza Track Selector")
    def debug(self, message):
        """Log a debug message"""
        self.logs.debug(message)
    def info(self, message):
        """Log an info message"""
        self.logs.info(message)
    def error(self, message):
        """Log an error message"""
        self.logs.error(message)
    def critical(self, message):
        """Log a critical message"""
        self.logs.critical(message)
    def set_level(self, level):
        """Set the log level"""
        self.logs.set_level(level)

class Settings:
    """Class to manage the app settings"""
    def __init__(self, app):
        self.logs = app.logs
        self.file = app.file
        self.settings = {
            'APPEARANCE': 'System',
            'UPGRADE_TRACKER': 'Yes',
            'UPGRADE_INTERVAL': '3',
            'NO_REPEAT': 'Yes'
        }
    def validate(self):
        """Check if the settings file exists and contains the required settings"""
        # Check if the settings file exists
        x = utilities.Files.check_exist(self.file)
        if x['success'] and x['result']:
            self.logs.debug(f'File exists: {self.file}')
        elif x['success'] and not x['result']:
            y = utilities.Files.create(self.file)
            # Verify creation
            if y['success']:
                self.logs.debug(f"File created: {self.file}")
            else:
                self.logs.error(f"Error creating file: {y['result']}")
        else:
            self.logs.error(x['result'])
        # Check each setting to verify its in the INI
        for key, value in self.settings.items():
            z = utilities.Ini.load(self.file, 'APP', key)
            if z['success']:
                self.logs.debug(f"Read {key} = {z['result']} from {self.file}")
            else:
                self.logs.error(f"Error reading {key} from {self.file}")
                self.logs.error(z['result'])
                # Write the default value
                a = utilities.Ini.write(self.file, 'APP', key, value)
                if a['success']:
                    self.logs.debug(f"Wrote {key} = {value} to {self.file}")
                else:
                    self.logs.error(f"Error writing {key} = {value} to {self.file}")
                    self.logs.error(a['result'])

    def modify(self, key: str, value: str):
        """Modify a setting in the settings file"""
        x = utilities.Ini.write(self.file, 'APP', key, value)
        if x['success']:
            self.logs.debug(f"Wrote {key} = {value} to {self.file}")
        else:
            self.logs.error(f"Error writing {key} = {value} to {self.file}")
            self.logs.error(x['result'])

    def read(self, key: str) -> dict:
        """Read a setting from the settings file"""
        x = utilities.Ini.load(self.file, 'APP', key)
        if x['success']:
            self.logs.debug(f"Read {key} = {x['result']} from {self.file}")
        else:
            self.logs.error(f"Error reading {key} from {self.file}")
            self.logs.error(x['result'])
        return x

class Roll:
    """Class to manage randomization"""
    # pylint: disable=too-many-instance-attributes
    # To be reviewed further
    def __init__(self, app):
        self.logs = app.logs
        self.history = app.history
        self.settings = app.settings
        self.layout_text = app.layout_text
        self.location_text = app.location_text
        self.weather_text = app.weather_text
        self.time_text = app.time_text
        self.app = app

    def track(self):
        """Randomly select a location and layout"""
        number_of_locations = len(options.tracks_list)
        self.logs.debug(f"Loaded {number_of_locations} locations from options.py")
        locations_index = number_of_locations - 1

        # If no-repeat is enabled, try to avoid selecting the same location
        location_int = random.randint(0, locations_index)
        location_name = options.tracks_list[location_int]['location']

        # If the location repeats and no-repeat is enabled, re-roll
        x = utilities.Ini.load(self.settings.file, 'APP', 'NO_REPEAT')
        if x['success']:
            if x['result'] == 'Yes':
                # Ensure that we don't pick the same location twice in a row
                while location_name == self.location_text.cget("text"):
                    self.logs.debug(f"Re-rolling location {location_name}")
                    location_int = random.randint(0, locations_index)
                    location_name = options.tracks_list[location_int]['location']

        self.logs.info(f"Selected location: {location_name}")

        # Get number of layouts for the selected location, then randomly select one
        number_of_layouts = len(options.tracks_list[location_int]['layout'])
        self.logs.debug(f"Found {number_of_layouts} layout(s) for {location_name}")
        layouts_index = number_of_layouts - 1
        layout_int = random.randint(0, layouts_index)
        layout_name = options.tracks_list[location_int]['layout'][layout_int]
        self.logs.info(f"Selected layout: {layout_name}")

        # Check if no-repeat is enabled, If no-repeat is set, add to the list of used layouts
        x = self.settings.read('NO_REPEAT')
        if x['success']:
            if x['result'] == 'Yes':
                # Check if this location was just used, re-roll if required
                if self.history.check(location_name, layout_name):
                    self.logs.debug("Combo exists in history. re-rolling..")
                    self.track()
                else:
                    self.history.add(location_name, layout_name)
            elif x['result'] == 'No':
                self.logs.debug("No-repeat not enabled. Not adding to history list.")
        elif not x['success']:
            self.logs.error(f"Error checking {self.settings.file} for 'NO_REPEAT'")
            self.logs.error(x['result'])

        self.layout_text.configure(text=layout_name)
        self.location_text.configure(text=location_name)

    def weather(self):
        """Randomly select a weather condition"""
        self.logs.debug("Rolling for weather..")
        selected_weather = options.weather_list[random.randint(0, len(options.weather_list) - 1)]
        self.logs.debug(f"Selected weather: {selected_weather}")
        self.weather_text.configure(text=selected_weather)

    def time(self):
        """Randomly select a time of day"""
        self.logs.debug("Rolling for time..")
        selected_time = options.time_of_day[random.randint(0, len(options.time_of_day) - 1)]
        self.logs.debug(f"Selected time: {selected_time}")
        self.time_text.configure(text=selected_time)


class History:
    """Class to manage the session history"""
    # pylint: disable=too-many-instance-attributes
    # To be reviewed further
    def __init__(self, app):
        self.logs = app.logs
        self.settings = app.settings
        self.total_races = 0
        self.total_races_text = app.total_races_text
        self.layout_text = app.layout_text
        self.location_text = app.location_text
        self.weather_text = app.weather_text
        self.time_text = app.time_text
        self.session_history = [
            {'location': "", "layout": []}
        ]

    def add(self, location: str, layout: str) -> dict:
        """Add the location and layout to the session history"""
        self.logs.debug("Starting loop")
        for track in self.session_history:
            if track['location'] == location:
                self.logs.debug(f"{track} found")
                if layout not in track['layout']:
                    track['layout'].append(layout)
                    self.logs.debug(f"{track} added")
                return
        self.session_history.append({'location': location, 'layout': [layout]})
        self.logs.debug(f"New track added: {location} - {layout}")

    def update_total(self):
        """Update the total races in session history"""
        self.total_races +=1
        self.logs.debug(f"Updating total races to {self.total_races}")
        self.total_races_text.configure(text=self.total_races)

    def reset(self):
        """Reset the history of tracks and layouts"""
        self.logs.info("RESETTING HISTORY!")
        self.session_history = []
        self.total_races = 0
        self.total_races_text.configure(text=self.total_races)
        self.location_text.configure(text="")
        self.layout_text.configure(text="")
        self.weather_text.configure(text="")
        self.time_text.configure(text="")

    def check(self, location: str, layout: str) -> bool:
        """Check if the location and layout exists in the session history"""
        for track in self.session_history:
            if track['location'] == location and layout in track['layout']:
                self.logs.debug(f"Exists in  history: {location} - {layout}")
                return True
        return False

App().mainloop()
