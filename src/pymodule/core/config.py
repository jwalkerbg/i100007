# core/config.py

import os
import sys
from typing import Dict, Any, Mapping, TypedDict
import argparse
from jsonschema import validate, ValidationError

from pymodule.logger import get_app_logger

logger = get_app_logger(__name__)

# Check Python version at runtime
if sys.version_info >= (3, 11):
    import tomllib as toml # Use the built-in tomllib for Python 3.11+
else:
    import tomli as toml # Use the external tomli for Python 3.7 to 3.10

class TemplateConfig(TypedDict, total=False):
    template_name: str
    template_version: str
    template_description: Dict[str, Any]

class LoggingConfig(TypedDict, total=False):
    verbose: bool
    version_option: bool

class ParametersConfig(TypedDict, total=False):
    param1: int
    param2: int

class PositionalsConfig(TypedDict, total=False):
    input_file: str
    output_file: str

class ConfigDict(TypedDict):
    template: TemplateConfig
    logging: LoggingConfig
    parameters: ParametersConfig
    positionals: PositionalsConfig

class Config:
    def __init__(self) -> None:
        self.config: ConfigDict = self.DEFAULT_CONFIG

    DEFAULT_CONFIG: ConfigDict = {
        'template': {
            'template_name': "pymodule",
            'template_version': "3.4.1",
            'template_description': { 'text': """Template with CLI interface, configuration options in a file, logger and unit tests""", 'content-type': "text/plain" }
        },
        'logging': {
            'verbose': False,
            'version_option': False
        },
        'parameters': {
            'param1': 1,
            'param2': 2
        },
        'positionals': {
            'input_file': '',
            'output_file': ''
        }
    }

    # When adding / removing changing configuration parameters, change following validation appropriately
    CONFIG_SCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "logging": {
                "type": "object",
                "properties": {
                    "verbose": {
                        "type": "boolean"
                    },
                    "version_option": {
                        "type": "boolean"
                    }
                },
                "additionalProperties": False
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "number"
                    },
                    "param2": {
                        "type": "number"
                    }
                },
                "additionalProperties": False
            },
            "positionals": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string"
                    },
                    "output_file": {
                        "type": "string"
                    }
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    }

    def load_toml(self,file_path:str) -> Dict[str, Any]:
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
                return toml.load(f)

        except FileNotFoundError as e:
            logger.error("%s",str(e))
            raise e  # Optionally re-raise the exception if you want to propagate it
        except toml.TOMLDecodeError as e:
            logger.error("Error: Failed to parse TOML file '%s'. Invalid TOML syntax.",file_path)
            raise e  # Re-raise the exception for further handling
        except Exception as e:
            logger.error("An unexpected error occurred while loading the TOML file: %s",str(e))
            raise e  # Catch-all for any other unexpected exceptions

    def load_config_file(self, file_path: str="config.toml") -> Dict[str, Any]:
        # skip the configuration file if an empty name is given
        if file_path == '':
            return {}
        # Convert None to default value of 'config.json'
        if file_path == "config.toml":
            logger.warning("CFG: Using default '%s'",file_path)
            file_path = 'config.toml'
        try:
            config_file = self.load_toml(file_path=file_path)
            validate(instance=config_file, schema=self.CONFIG_SCHEMA)
        except ValidationError as e:
            logger.warning("Configuration validation error in %s: %s",file_path,str(e))
            raise ValueError from e
        except Exception as e:
            logger.error("Exception when trying to load %s: %s",file_path,str(e))
            raise e

        self.deep_update(config=self.config, config_file=config_file)

        return config_file

    def deep_update(self,config:Mapping[str, Any], config_file: Dict[str, Any]) -> None:
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
                # Otherwise, update the key with the new value from config_file if it is present there
                if value is not None:
                    config[key] = value

    def load_config_env(self) -> ConfigDict:
        """
        Load configuration from environment variables.

        :return: Updated configuration dictionary
        """
        env_overrides = {
            "parameters": {
                "param1": os.getenv("PYMODULE_PARAM1"),
                "param2": os.getenv("PYMODULE_PARAM2")
            },
            "positionals": {
                "input_file": os.getenv("PYMODULE_INPUT_FILE"),
                "output_file": os.getenv("PYMODULE_OUTPUT_FILE")
            }
        }
        self.deep_update(config=self.config, config_file=env_overrides)

        return self.config

    def merge_cli_options(self, config_cli: argparse.Namespace | None = None) -> ConfigDict:    # pylint: disable=too-many-branches
        # handle CLI options if started from CLI interface
        # replace param1 and param2 with actual parameters, defined in app:parse_args()
        if config_cli:

            if config_cli.version_option is not None:
                self.config['logging']['version_option'] = config_cli.version_option

            # Handle general options
            if config_cli.verbose is not None:
                self.config['logging']['verbose'] = config_cli.verbose

            # sample parameters that should be changed in real applications
            if config_cli.param1 is not None:
                self.config['parameters']['param1'] = config_cli.param1
            if config_cli.param2 is not None:
                self.config['parameters']['param2'] = config_cli.param2

            # positional parameters
            if hasattr(config_cli, 'input_file') and config_cli.input_file is not None:
                self.config['positionals']['input_file'] = config_cli.input_file
            if hasattr(config_cli, 'output_file') and config_cli.output_file is not None:
                self.config['positionals']['output_file'] = config_cli.output_file

        return self.config

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments, including nested options for mqtt and MS Protocol."""
    parser = argparse.ArgumentParser(description='My CLI App with Config File and Overrides', epilog=f'Priority: (lowest) defaults -> config file -> environment variables -> CLI options (highest)')

    # configuration file name
    parser.add_argument('--config', type=str, dest='config', default='config.toml',\
                        help="Name of the configuration file, default is 'config.toml'")
    parser.add_argument('--no-config', action='store_const', const='', dest='config',\
                        help="Do not use a configuration file (only defaults & options)")

    # version
    parser.add_argument('-v', dest='version_option', action='store_true', default = False, help='Show version information of the module')

    # Verbosity option
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('--verbose', dest='verbose', action='store_const',\
                                 const=True, help='Enable verbose mode')
    verbosity_group.add_argument('--no-verbose', dest='verbose', action='store_const',\
                                 const=False, help='Disable verbose mode')

    # application options & parameters
    param_group = parser.add_argument_group("Options")
    param_group.add_argument('--param1', dest='param1', type=int, help="Parameter1")
    param_group.add_argument('--param2', dest='param2', type=int, help="Parameter2")

    positional_group = parser.add_argument_group("Parameters")
    positional_group.add_argument('input_file', type=str, nargs="?", help="Input file")
    positional_group.add_argument('output_file', type=str, nargs="?", help="Output file")

    return parser.parse_args()

def get_app_configuration() -> Config:
    """Get the application configuration.

    This function initializes the Config class, loads the configuration file,
    applies environment variable overrides, and returns the final configuration.

    Returns:
        ConfigDict: The final application configuration.
    """

    # Step 1: Create config object with default configuration
    config_instance = Config()

    # Step 2: Parse command-line arguments
    args = parse_args()
    if args.version_option:
        # If version option is requested, skip loading other configurations
        config_instance.config['logging']['version_option'] = True
        return config_instance

    # Step 3: Try to load configuration from configuration file
    config_file = args.config
    try:
        config_instance.load_config_file(config_file)
    except Exception as e:
        logger.info("Error with loading configuration file. Giving up.\n%s",str(e))
        raise

    # Step 4: Load config from environment variables (if set)
    try:
        config_instance.load_config_env()
    except Exception as e:
        logger.info("Error with loading environment variables. Giving up.\n%s",str(e))
        raise

    # Step 5: Merge default config, config.json, and command-line arguments
    config_instance.merge_cli_options(args)

    return config_instance
