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
            
    def test_public_repos_url(self):
        """
        Test that public_repos returns the correct list of repository names.
        """
        org_name = "test_org"
        repos_data = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "GPL"}},
            {"name": "repo3", "license": None},
        ]
        
        with patch.object(GithubOrgClient, 'repos_payload', new_callable=PropertyMock) as mock_repos_payload:
            mock_repos_payload.return_value = repos_data
            client = GithubOrgClient(org_name)
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            self.assertEqual(client.public_repos("MIT"), ["repo1"])
            self.assertEqual(client.public_repos("GPL"), ["repo2"])
            self.assertEqual(client.public_repos("Apache"), [])


if __name__ == '__main__':
    unittest.main()
