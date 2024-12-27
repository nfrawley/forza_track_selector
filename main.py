import customtkinter, utilities, tracks, random
from pathlib import Path

# Init logging
logs = utilities.logs(app_name="Forza-Selector")
global_env = str(Path('Settings/global.env'))

# Init variables
session_history = {
    'location': "", "layout": []
}

# Create env if it doesn't exist
x = utilities.files.check_exist(global_env)
if x['success'] and x['result']:
    logs.debug(f'File exists: {global_env}')
elif x['success'] and not x['result']:
    y = utilities.files.create(global_env)
    # Verify creation
    match y['success']:
        case True:
            logs.debug(f"File created: {global_env}")
            settings = {
                'SETUP_REQUIRED': 'Yes',
                'APPEARANCE': 'System',
                'UPGRADE_TRACKER': 'Yes',
                'UPGRADE_INTERVAL': '3',
                'NO_REPEAT': 'Yes'
            }
            for key, value in settings.items():
                z = utilities.env.write(global_env, key, value)
                if z['success']:
                    logs.debug(f"Set {key} = {value} in {global_env}")
                else:
                    logs.error(f"Couldn't write {key} = {value} in {global_env}")
                    logs.error(f"{z['result']}")
        case False: 
            logs.error(f"Error creating file: {y['result']}")
else:
    logs.error(x['result'])

def random_selection():
    # Get number of locations, then randomly select one
    number_of_locations = len(tracks.tracks_list)
    logs.debug(f"Loaded {number_of_locations} locations from tracks.py")
    locations_index = number_of_locations - 1
    selected_location_int = random.randint(0, locations_index)
    selected_location_name = tracks.tracks_list[selected_location_int]['location']
    logs.info(f"Selected location: {selected_location_name}")

    # Get number of layouts for the selected location, then randomly select one
    number_of_layouts = len(tracks.tracks_list[selected_location_int]['layout'])
    logs.debug(f"Found {number_of_layouts} layout(s) for {selected_location_name}")
    layouts_index = number_of_layouts - 1
    selected_layout_int = random.randint(0, layouts_index)
    selected_layout_name = tracks.tracks_list[selected_location_int]['layout'][selected_layout_int]
    logs.info(f"Selected layout: {selected_layout_name}")

    # If no-repeat is set, add to the list of used layouts
    x = utilities.env.load(global_env, 'NO_REPEAT')
    if x['success']:
        match x['result']:
            case 'Yes':
                # Add it to the historical list for session
                logs.debug("Adding to history list")
        
            case 'No':
                logs.debug("No-repeat not enabled. Not adding to history list.")
    elif not x['success']:
        logs.error(f"Error checking {global_env} for 'NO_REPEAT'")
        logs.error(x['result'])