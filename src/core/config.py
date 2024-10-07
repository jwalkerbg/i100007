# core/config.py

import sys
from typing import Dict
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

    def load_pyproject():
        try:
            # Attempt to load pyproject.toml from the package root
            with resources.path('pymodule', 'pyproject.toml') as pyproject_path:
                with open(pyproject_path, 'rb') as f:
                    if sys.version_info >= (3, 11):         # Use tomllib for Python 3.11+
                        pyproject_data = tomllib.load(f)
                    else:
                        pyproject_data = tomllib.load(f)    # Use tomli for Python 3.7 - 3.10
            return pyproject_data

        except FileNotFoundError:
            print("Error: 'pyproject.toml' not found in the package directory.")
            raise e
        except tomllib.TOMLDecodeError as e:
            print(f"Error: Failed to decode TOML file. Reason: {e}")
            raise e
        except OSError as e:
            print(f"Error: I/O error while accessing 'pyproject.toml'. Reason: {e}")
            raise e

    def load_configs(self, file_path:str) -> None:
        self.config = self.load_toml(file_path=file_path)
        self.pyproject_config = self.load_pyproject()

# # Example usage
# try:
#     config = load_toml("config.toml")
#     print("Config loaded successfully:", config)
# except Exception as e:
#     print(f"Failed to load config: {e}")

# # Load and access project data
# pyproject_data = load_pyproject()

# if pyproject_data:
#     project_name = pyproject_data.get("project", {}).get("name", "Unknown")
#     print(f"Project Name: {project_name}")
