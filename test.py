from pathlib import Path

# Define your patterns
patterns = ["*.c", "*.pyx", "*.py"]

# Use rglob for each pattern and combine results
files = [file for pattern in patterns for file in Path(".").rglob(pattern)]

for file in files:
    print(file)

print("ended")