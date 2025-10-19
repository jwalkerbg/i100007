# src/cli/app.py

from importlib.metadata import version as pkg_version

import pymodule
from pymodule.core.config import get_app_configuration
from pymodule.logger import get_app_logger
from pymodule.core.app_runner import run_app

logger = get_app_logger(__name__)

def main() -> None:
    """Main entry point of the CLI."""

    # Step 1: Collect configuration from defaults, configuration file, and environment variables and CLI options
    cfg = get_app_configuration()

    # Step 2: Show version info or run the application with collected configuration
    if cfg.config['logging']['version_option']:
        # Step 2a: Show version information
        logger.info("Version information requested")
        app_version = pkg_version("pymodule")
        print(f"pymodule {app_version}")
    else:
        # Step 2b: Run the application with the collected configuration
        run_app(cfg)

if __name__ == "__main__":
    main()
