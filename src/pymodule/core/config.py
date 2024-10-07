# core/config.py

import sys
from typing import Dict, Any
import importlib.resources as resources

# Check Python version at runtime
if sys.version_info >= (3, 11):
    import tomllib  # Use the built-in tomllib for Python 3.11+
else:
    import tomli  # Use the external tomli for Python 3.7 to 3.10

class Config:
    def __init__(self) -> None:
        self.config = {}
        self.pyproject_config = {}

    DEFAULT_CONFIG = {
        'template': {
            'template_name': "cliapp",
            'template_version': "0.2.0",
            'template_description': { 'text': """Template with CLI interface, configuration options in file and unit tests""", 'content-type': "text/plain" }
        },
        'logging': {
            'verbose': True
        },
        'parameters': {
            'param1': 1,
            'param2': 2
        }
    }

    def load_toml(self,file_path) -> Dict:
        """
        Load a TOML file with exception handling.

        :param file_path: Path to the TOML file
        :return: Parsed TOML data as a dictionary
        :raises FileNotFoundError: If the file does not exist
        :raises tomli.TOMLDecodeError / tomllib.TOMLDecodeError: If there is a parsing error
        """
        try:
            # Open the file in binary mode (required by both tomli and tomllib)
            with open(file_path, 'rb') as f:
                if sys.version_info >= (3, 11):
                    return tomllib.load(f)  # Use tomllib for Python 3.11+
                else:
                    return tomli.load(f)  # Use tomli for Python 3.7 - 3.10

        except FileNotFoundError as e:
            print(f"Error: File '{file_path}' not found.")
            raise e  # Optionally re-raise the exception if you want to propagate it
        except (tomli.TOMLDecodeError if sys.version_info < (3, 11) else tomllib.TOMLDecodeError) as e:
            print(f"Error: Failed to parse TOML file '{file_path}'. Invalid TOML syntax.")
            raise e  # Re-raise the exception for further handling
        except Exception as e:
            print(f"An unexpected error occurred while loading the TOML file: {e}")
            raise e  # Catch-all for any other unexpected exceptions

    def load_configs(self, file_path:str) -> None:
        self.config = self.load_toml(file_path=file_path)

    def deep_update(self,config: Dict[str, Any], config_file: Dict[str, Any]) -> None:
        """
        Recursively updates a dictionary (`config`) with the contents of another dictionary (`config_file`).
        It performs a deep merge, meaning that if a key contains a nested dictionary in both `config`
        and `config_file`, the nested dictionaries are merged instead of replaced.

        Parameters:
        - config (Dict[str, Any]): The original dictionary to be updated.
        - config_file (Dict[str, Any]): The dictionary containing updated values.

        Returns:
        - None: The update is done in place, so the `config` dictionary is modified directly.
        """
        for key, value in config_file.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                # If both values are dictionaries, recurse to merge deeply
                self.deep_update(config[key], value)
            else:
                # Otherwise, update the key with the new value from config_file
                config[key] = value

    def merge_options(self, config_file:Dict, config_cli=None) -> Dict:

        self.config = self.DEFAULT_CONFIG

        # handle CLI options if started from CLI interface
        if config_cli:
            if config_cli.param1:
                self.config['parameters']['param1'] = config_cli.param1
            if config_cli.param2:
                self.config['parameters']['param2'] = config_cli.param2

        # Handle general options
        if config_cli.verbose is not None:
            self.config['logging']['verbose'] = config_cli.verbose

        return self.config