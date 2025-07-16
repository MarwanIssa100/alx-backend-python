#!/usr/bin/env python3
from utils import access_nested_map , get_json
import unittest
from unittest.mock import MagicMock
from parameterized import parameterized
import requests

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ( {"a": 1}, ("a",), 1 ),
        ( {"a": {"b": 2}}, ("a",),{"b":2}),
        ( {"a": {"b": 2}}, ("a", "b"), 2 ),  # empty path returns the map itself
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ( {"a": 1}, ("b",), "b" ),
        ( {"a": {"b": 2}}, ("a", "c"), "c" ),
        ( {"a": {"b": 2}}, ("a", "b", "c"), "c" ),
        ( {"a": {"b": {"c": 42}}}, ("a", "x"), "x" ),
        ( {"a": 1}, ("a", "b"), "b" ),
    ])
    def test_access_nested_map_missing_key(self, nested_map, path, missing_key):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], missing_key)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
            
    def test_get_json(self):
        url = "https://api.github.com"
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        requests.get = MagicMock(return_value=mock_response)

        result = get_json(url)
        self.assertEqual(result, {"key": "value"})
        requests.get.assert_called_once_with(url)

if __name__ == '__main__':
    unittest.main()    