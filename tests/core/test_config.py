# tests/test_core_module_a.py

import unittest
import pytest
from pymodule import core

#############

class TestConfig:

    @pytest.fixture
    def cfg(self):
        """
        Fixture to create an instance of ConfigUpdater for testing.
        This fixture is used to provide a reusable instance of the class
        in each test case to ensure clean setup.
        """
        return core.Config()

    def test_deep_update_with_nested_dicts(self, cfg):
        """
        Test case: Deep update with nested dictionaries.
        Scenario: When both `config` and `config_file` have nested dictionaries,
        ensure that the update merges the inner dictionaries correctly.
        """
        config = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            }
        }
        config_file = {
            'b': {
                'd': 4,   # Value that should update the existing 'd'
                'e': 5    # New key that should be added to the dictionary
            },
            'f': 6      # New key that should be added at the top level
        }
        cfg.deep_update(config, config_file)

        expected = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 4,  # Updated value from 3 to 4
                'e': 5   # Added new key-value pair
            },
            'f': 6      # Added new key-value pair at the top level
        }
        assert config == expected

    def test_deep_update_with_non_dict(self, cfg):
        """
        Test case: Update with non-dictionary values.
        Scenario: If the value in `config_file` is not a dictionary, it should
        overwrite the value in `config`, regardless of its type.
        """
        config = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            }
        }
        config_file = {
            'a': 100,  # Should replace the value of 'a'
            'b': {
                'c': 200  # Should replace the value of 'c' inside 'b'
            }
        }
        cfg.deep_update(config, config_file)

        expected = {
            'a': 100,   # Updated from 1 to 100
            'b': {
                'c': 200,  # Updated from 2 to 200
                'd': 3     # Unchanged because it was not present in `config_file`
            }
        }
        assert config == expected

    def test_deep_update_with_no_changes(self, cfg):
        """
        Test case: No changes needed.
        Scenario: If all values in `config_file` match those in `config`,
        there should be no updates made.
        """
        config = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            }
        }
        config_file = {
            'a': 1,    # No change
            'b': {
                'c': 2   # No change
            }
        }
        cfg.deep_update(config, config_file)

        expected = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3  # Remains the same
            }
        }
        assert config == expected

    def test_deep_update_with_empty_dict(self, cfg):
        """
        Test case: Update with an empty dictionary.
        Scenario: If `config_file` is empty, the original `config` should remain unchanged.
        """
        config = {
            'a': 1,
            'b': {
                'c': 2,
            }
        }
        config_file = {}  # Empty dictionary, no changes should occur
        cfg.deep_update(config, config_file)

        expected = {
            'a': 1,
            'b': {
                'c': 2,
            }
        }
        assert config == expected

    def test_deep_update_with_nested_and_flat_keys(self, cfg):
        """
        Test case: Mix of nested and flat keys.
        Scenario: Tests both nested dictionary merging and flat key updates
        to ensure that deep and shallow updates work as expected.
        """
        config = {
            'a': {
                'b': {
                    'c': 3
                }
            },
            'd': 4
        }
        config_file = {
            'a': {
                'b': {
                    'c': 5,   # Update the value of 'c'
                    'e': 6    # Add a new key 'e' to the nested dictionary
                }
            },
            'd': 7   # Update the value of 'd' at the top level
        }
        cfg.deep_update(config, config_file)

        expected = {
            'a': {
                'b': {
                    'c': 5,  # Updated value from 3 to 5
                    'e': 6   # Added new key-value pair in nested dictionary
                }
            },
            'd': 7   # Updated from 4 to 7
        }
        assert config == expected
