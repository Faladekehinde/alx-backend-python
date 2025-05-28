#!/usr/bin/env python3
"""In this task you will write the first unit test
for utils.access_nested_map.Create a TestAccessNestedMap
class that inherits from unittest.TestCase.Implement the
TestAccessNestedMap.test_access_nested_map method to test
that the method returns what it is supposed to.Decorate
the method with @parameterized.expand to test the function
for following inputs:

    nested_map={"a": 1}, path=("a",)
    nested_map={"a": {"b": 2}}, path=("a",)
    nested_map={"a": {"b": 2}}, path=("a", "b")
For each of these inputs, test with assertEqual that the
function returns the test_payload result.The body of the test method
should not be longer than 2 lines."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """test the access nested map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, test_payload):
        """test the access nested map method"""
        self.assertEqual(access_nested_map(nested_map, path), test_payload)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, test_payload):
        """check that a KeyError is raised when the
        access_nested_map function is called with these parameters
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), test_payload)
        # self.assertEqual(f"KeyError('{test_payload}')", repr(err.exception))


class TestGetJson(unittest.TestCase):
    """tests get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """test that utils.get_json returns the expected result"""
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            response = get_json(test_url)
            mock_get.assert_called_ones_with(test_url)
            self.assertEqual(response, test_payload)


class TestMemoize(unittest.TestCase):
    """ test the memoize function"""

    def test_memoize(self):
        """ testing
        """

        class TestClass:
            """ Test Class for wrapping with memoize """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test_class = TestClass()
            response1 = test_class.a_property()
            response2 = test_class.a_property()

            #assert return value are correct
            self.assertEqual(response1, 42)
            self.assertEqual(response2, 42)

            # Assert a_method was called only once due to memoization
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()