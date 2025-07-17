#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
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
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, expected)


if __name__ == '__main__':
    unittest.main()
