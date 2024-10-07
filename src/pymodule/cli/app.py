# src/cli/app.py
import argparse

import pymodule.core.core_module_a
import pymodule.core.core_module_b
import pymodule.utils.utilities
import pymodule.drivers.ina236

from pymodule.core.config import Config

def parse_args():
    """Parse command-line arguments, including nested options for mqtt and MS Protocol."""
    parser = argparse.ArgumentParser(description='My CLI App with Config File and Overrides')

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

    cfg = Config()

    # Step 1: Load the default configuration from config.json
    cfg.load_config_file("config.toml")

    # Step 2: Parse command-line arguments
    args = parse_args()

    # Step 3: Merge default config, config.json, and command-line arguments
    cfg.merge_options(cfg.config, args)

    run_app(cfg)

def run_app(config:Config) -> None:
    print("Running run_app")

    print(f"config = {config.config}")

if __name__ == "__main__":
    main()
