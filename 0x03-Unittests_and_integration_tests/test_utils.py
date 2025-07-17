#!/usr/bin/env python3
"""Unit tests for utils module functions: access_nested_map, get_json, memoize."""

import unittest
from unittest.mock import Mock, patch

from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize,
)

# The class `TestAccessNestedMap` contains unit tests for
# the `access_nested_map` function.
# It tests retrieving values from nested dictionaries based on a given path.
class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 42}}}, ("a", "b", "c"), 42),
        ({"x": {"y": {"z": "found"}}}, ("x", "y", "z"), "found"),
        ({"a": 1}, (), {"a": 1}),  # empty path returns the map itself
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({"a": 1}, ("b",), "b"),
        ({"a": {"b": 2}}, ("a", "c"), "c"),
        ({"a": {"b": 2}}, ("a", "b", "c"), "c"),
        ({"a": {"b": {"c": 42}}}, ("a", "x"), "x"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_missing_key(
            self, nested_map, path, missing_key):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(
            cm.exception.args[0],
            missing_key
        )

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(
                nested_map,
                path
            )


# The class `TestGetJson` contains a unit test for the `get_json` function.
class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)


# The class `TestMemoize` contains a unit test for a memoization decorator
# applied to a method and property within a test class.
class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()
        with patch.object(
            test_instance,
            'a_method',
            return_value=42
        ) as mock_method:
            self.assertEqual(
                test_instance.a_property,
                42
            )
            mock_method.assert_called_once()
            self.assertEqual(
                test_instance.a_property,
                42
            )
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
