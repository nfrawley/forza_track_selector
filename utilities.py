"""Noah's common python utilities"""
import os
import logging
import datetime
import configparser

class Ini:
    """Interact with .ini files."""
    @staticmethod
    def get_sections(file: str) -> dict:
        """
        Check all the sections in a .ini file.

        Args:
            file (str): The path to the .ini file.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs. 
            'result' lists each section in the .ini, or a string of the exception that occurred.
        """
        try:
            config = configparser.ConfigParser()
            config.read(file)
            sections = config.sections()
            return {'success': True, 'result': sections}
        except (configparser.NoSectionError, configparser.NoOptionError,
                configparser.ParsingError, FileNotFoundError, IOError, OSError) as e:
            return {'success': False, 'result': str(e)}

    @staticmethod
    def load(file: str, section: str, key: str) -> dict:
        """
        Load the value of a key from a .ini file.

        Args:
            file (str): The path to the .ini file.
            section (str): The section of the key to load.
            key (str): The key to load.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs.
            'result' contains the value of requested key, or string of the exception that occurred.
        """
        try:
            config = configparser.ConfigParser()
            config.read(file)
            if section not in config:
                return {'success': False, 'result': f"Section '{section}' not found."}
            if key not in config[section]:
                return {'success': False, 'result': f"Key '{key}' not found: section '{section}'."}
            value = config[section][key]
            return {'success': True, 'result': value}
        except (configparser.NoSectionError, configparser.NoOptionError,
                configparser.ParsingError, FileNotFoundError, IOError, OSError) as e:
            return {'success': False, 'result': str(e)}

    @staticmethod
    def write(file: str, section: str, key: str, value: str) -> dict:
        """
        Write a value to a key in a .ini file.

        Args:
            file (str): The path to the .ini file.
            section (str): The section of the key to modify.
            key (str): The key to modify.
            value (str): The value of the key.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs.
            'result' contains the value of the set key, or a string of the exception that occurred.
        """
        try:
            if not Files.check_exist(file)['result']:
                Files.create(file)
            config = configparser.ConfigParser()
            config.read(file)
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, key, value)
            with open(file, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            return {'success': True, 'result': value}
        except (configparser.NoSectionError, configparser.ParsingError,
                FileNotFoundError, IOError) as e:
            return {'success': False, 'result': str(e)}

class Files:
    """Interact with files."""

    @staticmethod
    def check_exist(file: str) -> dict:
        """
        Check if a file exists.

        Args:
            file (str): The path to the file to check.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs.
            'result' contains True if file exists, False if the file does not exist -
            or a string of the exception that occurred.
        """
        try:
            with open(file, 'r', encoding='utf-8'):
                return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except (OSError, IOError) as e:
            return {'success': False, 'result': str(e)}

    @staticmethod
    def create(file: str) -> dict:
        """
        Create a file and its directories if they do not exist.

        Args:
            file (str): The path to the file to create.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs.
            'result' contains True if file was created, or a string of the exception that occurred.
        """
        try:
            print(f"Attempting to create file at: {file}")
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w', encoding='utf-8') as f:
                f.write('')
            return {'success': True, 'result': True}
        except (OSError, IOError) as e:
            return {'success': False, 'result': str(e)}


    @staticmethod
    def remove(file: str) -> dict:
        """
        Remove a file.

        Args:
            file (str): The path to the file to remove.

        Returns:
            dict: Dictionary with keys 'success' and 'result'.
            'success' is False if an exception occurs.
            'result' contains True if file was removed, False if the file was not found -
            or a string of the exception that occurred.
        """
        try:
            os.remove(file)
            return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except (OSError, IOError) as e:
            return {'success': False, 'result': str(e)}

class Logs:
    """Interact with logs."""

    def __init__(self, app_name: str, *args, **kwargs):
        """
        Start a logger for the app you're calling from.

        Args:
            app_name: Used to identify app (or section of app) adding to logfile.
        """
        # pylint: disable=too-many-localsßß
        # This is a reasonable amount of local variables for this functionß
        super().__init__(*args, **kwargs)

        # Define the path for Settings.ini relative to the current working directory
        log_settings = os.path.join(os.getcwd(), 'Settings.ini')

        # Check if 'Settings.ini' exists; if not, create it
        x = Files.check_exist(log_settings)
        if x['success'] and not x['result']:
            # If Settings.ini doesn't exist, create it and set default logging settings
            print(f"Settings.ini not found, creating it: {log_settings}")
            y = Files.create(log_settings)
            if y['success']:
                print(f"File created: {log_settings}")
                settings = {
                    'LOGGING_LEVEL': 'INFO',
                    'LOGGING_DIR': 'Logs/',
                }
                # Ensure 'LOGGING' section and default settings are written
                config = configparser.ConfigParser()
                config.read(log_settings)
                if not config.has_section('LOGGING'):
                    config.add_section('LOGGING')
                for key, value in settings.items():
                    config.set('LOGGING', key, value)
                # Write settings back to the config file
                with open(log_settings, 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
            else:
                print(f"Error creating file: {y['result']}")

        # Load the configuration settings for logging
        config = configparser.ConfigParser()
        config.read(log_settings)

        # Ensure the 'LOGGING' section exists before reading settings
        if not config.has_section('LOGGING'):
            print(f"Error: 'LOGGING' section missing in {log_settings}")
            level = 'INFO'  # Default to INFO if section is missing
        else:
            load_level = Ini.load(log_settings, 'LOGGING', 'LOGGING_LEVEL')
            level = load_level['result'] if load_level['success'] else 'INFO'

        # Set up logging
        self.app_logger = logging.getLogger()
        self.app = app_name
        today = datetime.datetime.now().strftime("%b-%d-%Y")
        log_path = f"Logs/{today}.log"

        # Ensure the 'Logs' directory exists before creating log file
        log_dir = 'Logs'
        x = Files.check_exist(log_dir)
        if x['success'] and not x['result']:
            os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Ensure log file is created
        x = Files.check_exist(log_path)
        if x['success'] and not x['result']:
            y = Files.create(log_path)
            if y['success']:
                print(f"Created {log_path}")
            else:
                print(f"Error creating file: {y['result']}")
        else:
            print(f"Log file exists: {log_path}")

        # Set up the logging configuration
        logging.basicConfig(filename=log_path, format="%(asctime)s - %(message)s")
        self.level = level.upper() if level else 'INFO'
        self.app_logger.setLevel(getattr(logging, self.level))
        print(f"Logging level set to: {level}")

    def set_level(self, level: str):
        """
        Sets the logging level.

        Args:
            level: Accepts (INFO/DEBUG/ERROR/CRITICAL).
        """
        new_level = level.upper()
        self.app_logger.setLevel(getattr(logging, new_level))
        print(f"Logging level updated to {new_level}")

    def info(self, message: str) -> None:
        """ Log an INFO entry. """
        self.app_logger.info("%s - INFO: %s", self.app, message)

    def debug(self, message: str) -> None:
        """ Log a DEBUG entry. """
        self.app_logger.debug("%s - DEBUG: %s", self.app, message)

    def error(self, message: str) -> None:
        """ Log an ERROR entry. """
        self.app_logger.error("%s - ERROR: %s", self.app, message)

    def critical(self, message: str) -> None:
        """ Log a CRITICAL entry. """
        self.app_logger.critical("%s - CRITICAL: %s", self.app, message)
