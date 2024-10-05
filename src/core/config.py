# core/config.py

import sys

# Check Python version at runtime
if sys.version_info >= (3, 11):
    import tomllib  # Use the built-in tomllib for Python 3.11+
else:
    import tomli  # Use the external tomli for Python 3.7 to 3.10

class Config:
    def __init__(self) -> None:
        self.config = {}

    def load_toml(self,file_path):
        """
        Load a TOML file with exception handling.

        :param file_path: Path to the TOML file
        :return: Parsed TOML data as a dictionary
        :raises FileNotFoundError: If the file does not exist
        :raises tomli.TOMLDecodeError / tomllib.TOMLDecodeError: If there is a parsing error
        """
        self.config = {}    # clear previous config
        try:
            # Open the file in binary mode (required by both tomli and tomllib)
            with open(file_path, 'rb') as f:
                if sys.version_info >= (3, 11):
                    self.config = tomllib.load(f)  # Use tomllib for Python 3.11+
                else:
                    self.config = tomli.load(f)  # Use tomli for Python 3.7 - 3.10
                return self.config

        except FileNotFoundError as e:
            print(f"Error: File '{file_path}' not found.")
            raise e  # Optionally re-raise the exception if you want to propagate it

        except (tomli.TOMLDecodeError if sys.version_info < (3, 11) else tomllib.TOMLDecodeError) as e:
            print(f"Error: Failed to parse TOML file '{file_path}'. Invalid TOML syntax.")
            raise e  # Re-raise the exception for further handling

        except Exception as e:
            print(f"An unexpected error occurred while loading the TOML file: {e}")
            raise e  # Catch-all for any other unexpected exceptions

# # Example usage
# try:
#     config = load_toml("config.toml")
#     print("Config loaded successfully:", config)
# except Exception as e:
#     print(f"Failed to load config: {e}")
