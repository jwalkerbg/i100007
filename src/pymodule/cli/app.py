# src/cli/app.py
import argparse

import pymodule.core.core_module_a
import pymodule.core.core_module_b
import pymodule.utils.utilities
import pymodule.drivers.ina236

from pymodule.core.config import Config
from pymodule.logger.logger_module import logger, string_handler

def parse_args():
    """Parse command-line arguments, including nested options for mqtt and MS Protocol."""
    parser = argparse.ArgumentParser(description='My CLI App with Config File and Overrides')

    # configuration file name
    parser.add_argument('--config', type=str,default='config.toml',help="Name of the configuration file, default is 'config.toml'")

    # parameters
    parser.add_argument('--param1', type=int, help="Parameter1")
    parser.add_argument('--param2', type=int, help="Parameter2")

    # Other general options can still be added
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('--verbose', dest='verbose', action='store_const', const=True, help='Enable verbose mode')
    verbosity_group.add_argument('--no-verbose', dest='verbose', action='store_const', const=False, help='Disable verbose mode')

    return parser.parse_args()

def main():
    """Main entry point of the CLI."""

    # Step 1: Create config object with default configuration
    cfg = Config()

    # Step 2: Parse command-line arguments
    args = parse_args()

    # Step 3: Try to load configuration from configuration file
    config_file = args.config
    try:
        cfg.load_config_file(config_file)
    except Exception as e:
        logger.info(f"Error with loading configuration file. Giving up.")
        return

    # Step 4: Merge default config, config.json, and command-line arguments
    cfg.merge_options(cfg.config, args)

    # Step 5: Run the application with collected configuration
    run_app(cfg)

def run_app(config:Config) -> None:
    logger.info("Running run_app")

    logger.info(f"config = {config.config}")
    pymodule.core.core_module_a.hello_from_core_module_a()
    pymodule.core.core_module_a.goodbye_from_core_module_a()
    pymodule.core.core_module_b.hello_from_core_module_b()
    pymodule.core.core_module_b.goodbye_from_core_module_b()

if __name__ == "__main__":
    main()
