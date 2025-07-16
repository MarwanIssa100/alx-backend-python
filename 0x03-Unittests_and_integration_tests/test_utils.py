from utils import access_nested_map
from pytest import raises

def test_access_nested_map():
    nested_map = {"a": {"b": {"c": 1}}}
    assert access_nested_map(nested_map, ["a", "b", "c"]) == 1
    assert access_nested_map(nested_map, ["a", "b"]) == {"c": 1}
    
def test_access_nested_map_missing_key():
    nested_map = {"a": {"b": {"c": 1}}}
    with raises(KeyError):
        access_nested_map(nested_map, ["a", "b", "d"])
    