# src/cli/app.py
import argparse

import utils.utilities
import drivers.ina236
import manufacturing_client.mfclient

def main():
    parser = argparse.ArgumentParser(description="CLI Tool for My Project")
    parser.add_argument("--version", action="version", version="pymodule 0.1.0")

    # Define subcommands
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Example command: greet
    greet_parser = subparsers.add_parser("greet", help="Greet the user")
    greet_parser.add_argument("name", type=str, help="Name of the person to greet")

    # Example command: add
    add_parser = subparsers.add_parser("add", help="Add two numbers")
    add_parser.add_argument("x", type=int, help="First number")
    add_parser.add_argument("y", type=int, help="Second number")

    # Parse the arguments
    args = parser.parse_args()

    # Handle the commands
    if args.command == "greet":
        print(f"Hello, {args.name}!")
    elif args.command == "add":
        result = args.x + args.y
        print(f"The sum of {args.x} and {args.y} is {result}")
    else:
        parser.print_help()

    print(f"\nCalls hello functions from modules")
    print(f"----------------------------------")
    utils.hello_from_utils()
    drivers.hello_from_ina236()
    manufacturing_client.hello_from_mfclient()
    print(f"----------------------------------")

if __name__ == "__main__":
    main()
