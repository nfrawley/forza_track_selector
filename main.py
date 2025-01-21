"""Noah's improved Forza Track Selector"""
import random
import customtkinter
import options
import utilities

class App(customtkinter.CTk):
    """Main application class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Forza Track Selector")
        self.geometry("800x480")
        # Init logging
        self.logs = utilities.Logs(app_name="Forza Track Selector")
        # Init variables
        self.file = 'Settings.ini'
        self.settings = {
            'APPEARANCE': 'System',
            'UPGRADE_TRACKER': 'Yes',
            'UPGRADE_INTERVAL': '3',
            'NO_REPEAT': 'Yes'
        }
        self.session_history = [
            {'location': "", "layout": []}
        ]
        self.total_races = 0

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
        self.random_button = customtkinter.CTkButton(self.buttons_frame, text="Random Track", command=lambda: [self.roll.track(), self.update_total()])
        self.random_button.grid(row=0, column=0, padx=10, pady=10)
        self.reset_button = customtkinter.CTkButton(self.buttons_frame, text="Reset", command=self.reset_history)
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
        self.total_races_text = customtkinter.CTkLabel(self.stats_frame, text=self.total_races)
        self.total_races_text.grid(row=1, column=1, padx=10, pady=10)

        self.settings = Settings(self)
        self.roll = Roll(self)
        self.history = History(self)
        self.settings.validate()

    def history_check(self, location: str, layout: str) -> bool:
        """Check if the location and layout exists in the session history"""
        for track in self.session_history:
            if track['location'] == location and layout in track['layout']:
                self.logs.debug(f"Exists in  history: {location} - {layout}")
                return True
        return False

    def reset_history(self):
        """Reset the history of tracks and layouts"""
        self.logs.info("RESETTING HISTORY!")
        self.logs.debug("But First, here's the history:")
        self.logs.debug(self.session_history)
        self.session_history = [
            {'location': "", "layout": []}
        ]
        self.total_races = 0
        self.total_races_text.configure(text=self.total_races)
        self.location_text.configure(text="")
        self.layout_text.configure(text="")
        self.weather_text.configure(text="")
        self.time_text.configure(text="")

    def random_weather(self):
        """Randomly select a weather condition"""
        self.logs.debug("Rolling for weather..")
        selected_weather = options.weather_list[random.randint(0, len(options.weather_list) - 1)]
        self.logs.debug(f"Selected weather: {selected_weather}")
        self.weather_text.configure(text=selected_weather)

    def random_time(self):
        """Randomly select a time of day"""
        self.logs.debug("Rolling for time..")
        selected_time = options.time_of_day[random.randint(0, len(options.time_of_day) - 1)]
        self.logs.debug(f"Selected time: {selected_time}")
        self.time_text.configure(text=selected_time)

    def update_total(self):
        """Add 1 to the total races count"""
        self.total_races +=1
        self.logs.debug(f"Updating total races to {self.total_races}")
        self.total_races_text.configure(text=self.total_races)

class Settings:
    """Class to manage the app settings"""
    def __init__(self, app):
        self.logs = app.logs
        self.settings = app.settings
        self.file = app.file
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

class Roll:
    """Class to manage randomization"""
    def __init__(self, app):
        self.logs = app.logs
        self.settings = app.settings
        self.history = app.session_history
        self.layout_text = app.layout_text
        self.location_text = app.location_text
        self.app = app
    def track(self):
        """Randomly select a location and layout"""
        number_of_locations = len(options.tracks_list)
        self.logs.debug(f"Loaded {number_of_locations} locations from options.py")
        locations_index = number_of_locations - 1

        # If no-repeat is enabled, try to avoid selecting the same location
        selected_location_int = random.randint(0, locations_index)
        selected_location_name = options.tracks_list[selected_location_int]['location']

        # If the location repeats and no-repeat is enabled, re-roll
        x = utilities.Ini.load(self.settings.file, 'APP', 'NO_REPEAT')
        if x['success']:
            if x['result'] == 'Yes':
                # Ensure that we don't pick the same location twice in a row
                while selected_location_name == self.location_text.cget("text"):
                    self.logs.debug(f"Re-rolling location to avoid repeating {selected_location_name}")
                    selected_location_int = random.randint(0, locations_index)
                    selected_location_name = options.tracks_list[selected_location_int]['location']

        self.logs.info(f"Selected location: {selected_location_name}")

        # Get number of layouts for the selected location, then randomly select one
        number_of_layouts = len(options.tracks_list[selected_location_int]['layout'])
        self.logs.debug(f"Found {number_of_layouts} layout(s) for {selected_location_name}")
        layouts_index = number_of_layouts - 1
        selected_layout_int = random.randint(0, layouts_index)
        selected_layout_name = options.tracks_list[selected_location_int]['layout'][selected_layout_int]
        self.logs.info(f"Selected layout: {selected_layout_name}")

        # If no-repeat is set, add to the list of used layouts
        if x['success']:
            if x['result'] == 'Yes':
                # Check if this location was just used, re-roll if required
                if App.history_check(self.app, selected_location_name, selected_layout_name):
                    self.logs.debug(f"{selected_location_name}: {selected_layout_name} exists in history. re-rolling..")
                    self.track()
                else:
                    self.app.history.add(selected_location_name, selected_layout_name)
            elif x['result'] == 'No':
                self.logs.debug("No-repeat not enabled. Not adding to history list.")
        elif not x['success']:
            self.logs.error(f"Error checking {self.settings.file} for 'NO_REPEAT'")
            self.logs.error(x['result'])

        self.layout_text.configure(text=selected_layout_name)
        self.location_text.configure(text=selected_location_name)
        self.app.random_weather()
        self.app.random_time()

class History:
    """Class to manage the session history"""
    def __init__(self, app):
        self.logs = app.logs
        self.settings = app.settings
        self.history = app.session_history
    def add(self, location: str, layout: str) -> dict:
        """Add the location and layout to the session history"""
        self.logs.debug("Starting loop")
        for track in self.history:
            if track['location'] == location:
                self.logs.debug(f"{track} found")
                if not layout in track['layout']:
                    track['layout'].append(layout)
                    self.logs.debug(f"{track} added")
            else:
                self.history.append({'location': location, 'layout': [layout]})
App().mainloop()
