#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("microsoft", {"login": "microsoft", "id": 2}),
    ])
    def test_org(self, org_name, expected):
        """
        Test that the org method returns the correct organization data.
        """
        with patch('client.GithubOrgClient.org', return_value=expected) as mock_org:
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, expected)
            mock_org.assert_called_once_with(org_name)


if __name__ == '__main__':
    unittest.main()
