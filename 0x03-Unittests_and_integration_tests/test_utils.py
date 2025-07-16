#!/usr/bin/env python3
from utils import access_nested_map
import unittest
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    
    @parameterized.expand([
        ({"a": {"b": {"c": 42}}}, ("a", "b", "c"), 42)])
    def test_access_nested_map(self):
        nested_map = {"a": {"b": {"c": 42}}}
        self.assertEqual(access_nested_map(nested_map, ("a", "b", "c")), 42)
        
    def test_access_nested_map_missing_key(self):
        nested_map = {"a": {"b": {"c": 42}}}
        with self.assertRaises(KeyError, msg="KeyError should be raised"):
            access_nested_map(nested_map, ("a", "b", "d"))

if __name__ == '__main__':
    unittest.main()    