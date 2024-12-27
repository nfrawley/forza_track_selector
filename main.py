import customtkinter, utilities, tracks, random
from pathlib import Path

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Forza Track Selector")
        self.geometry("800x480")
        # Init logging
        self.logs = utilities.logs(app_name="Forza-Selector")
        self.global_env = str(Path('Settings/global.env'))

        # Init variables
        self.session_history = [
            {'location': "", "layout": []}
        ]

        # Create env if it doesn't exist
        x = utilities.files.check_exist(self.global_env)
        if x['success'] and x['result']:
            self.logs.debug(f'File exists: {self.global_env}')
        elif x['success'] and not x['result']:
            y = utilities.files.create(self.global_env)
            # Verify creation
            match y['success']:
                case True:
                    self.logs.debug(f"File created: {self.global_env}")
                    settings = {
                        'SETUP_REQUIRED': 'Yes',
                        'APPEARANCE': 'System',
                        'UPGRADE_TRACKER': 'Yes',
                        'UPGRADE_INTERVAL': '3',
                        'NO_REPEAT': 'Yes'
                    }
                    for key, value in settings.items():
                        z = utilities.env.write(self.global_env, key, value)
                        if z['success']:
                            self.logs.debug(f"Set {key} = {value} in {self.global_env}")
                        else:
                            self.logs.error(f"Couldn't write {key} = {value} in {self.global_env}")
                            self.logs.error(f"{z['result']}")
                case False: 
                    self.logs.error(f"Error creating file: {y['result']}")
        else:
            self.logs.error(x['result'])

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.random_button = customtkinter.CTkButton(self.frame, text="Random Track", command=self.random_selection)
        self.random_button.grid(row=1, column=0)

        self.location_label = customtkinter.CTkLabel(self.frame, text="Location:")
        self.location_label.grid(row=2, column=0)
        self.location_text = customtkinter.CTkLabel(self.frame, text="")
        self.location_text.grid(row=2, column=1)

        self.layout_label = customtkinter.CTkLabel(self.frame, text="Layout:")
        self.layout_label.grid(row=3, column=0)
        self.layout_text = customtkinter.CTkLabel(self.frame, text="")
        self.layout_text.grid(row=3, column=1)

        self.weather_label = customtkinter.CTkLabel(self.frame, text="Weather:")
        self.weather_label.grid(row=4, column=0)
        self.weather_text = customtkinter.CTkLabel(self.frame, text="TEST")
        self.weather_text.grid(row=4, column=1)

        self.reset_button = customtkinter.CTkButton(self.frame, text="Reset", command=self.reset_history)
        self.reset_button.grid(row=5, column=0)
        
    def random_selection(self):
        # Get number of locations, then randomly select one
        number_of_locations = len(tracks.tracks_list)
        self.logs.debug(f"Loaded {number_of_locations} locations from tracks.py")
        locations_index = number_of_locations - 1
        selected_location_int = random.randint(0, locations_index)
        selected_location_name = tracks.tracks_list[selected_location_int]['location']
        self.logs.info(f"Selected location: {selected_location_name}")

        # Get number of layouts for the selected location, then randomly select one
        number_of_layouts = len(tracks.tracks_list[selected_location_int]['layout'])
        self.logs.debug(f"Found {number_of_layouts} layout(s) for {selected_location_name}")
        layouts_index = number_of_layouts - 1
        selected_layout_int = random.randint(0, layouts_index)
        selected_layout_name = tracks.tracks_list[selected_location_int]['layout'][selected_layout_int]
        self.logs.info(f"Selected layout: {selected_layout_name}")

        # If no-repeat is set, add to the list of used layouts
        x = utilities.env.load(self.global_env, 'NO_REPEAT')
        if x['success']:
            match x['result']:
                case 'Yes':
                    # Add it to the historical list for session
                    self.logs.debug("Adding to history list")
                    self.history_add(selected_location_name, selected_layout_name)
                case 'No':
                    self.logs.debug("No-repeat not enabled. Not adding to history list.")
        elif not x['success']:
            self.logs.error(f"Error checking {self.global_env} for 'NO_REPEAT'")
            self.logs.error(x['result'])

        self.layout_text.configure(text=selected_layout_name)
        self.location_text.configure(text=selected_location_name)

    def history_add(self, location: str, layout: str) -> dict:
        self.logs.debug("Starting loop")
        for track in self.session_history:
            if track['location'] == location:
                self.logs.debug(f"{track} found")
                if layout in track['layout']:
                    break
                else:
                    track['layout'].append(layout)
                    self.logs.debug(f"{track} added")
                    break
            else:
                self.session_history.append({'location': location, 'layout': [layout]})
    
    def reset_history(self):
        self.logs.info("RESETTING HISTORY!")
        self.session_history = [
            {'location': "", "layout": []}
        ]
        self.location_text.configure(text="Press the button!")
        self.layout_text.configure(text="Press the button!")

App().mainloop()