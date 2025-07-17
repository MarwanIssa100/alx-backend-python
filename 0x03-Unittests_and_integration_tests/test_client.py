#!/usr/bin/env python3
"""
A github org client
"""
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
        Test that the org method
        returns the correct organization data.
        """
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = expected
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, expected)

    def test_public_repos_url(self):
        """
        Test that the _public_repos_url property returns the correct URL.
        """
        org_name = "test_org"
        expected_url = "https://api.github.com/orgs/test_org/repos"
        client = GithubOrgClient(org_name)
        self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repository names,
        and that get_json and _public_repos_url are called as expected.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        test_url = "http://test_url"
        org_name = "test_org"
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient(org_name)
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
            
    def test_has_license(self):
        """
        Test that has_license correctly identifies repositories with a specific license.
        """
        repo_with_license = {"license": {"key": "MIT"}}
        repo_without_license = {"license": None}
        self.assertTrue(GithubOrgClient.has_license(repo_with_license, "MIT"))
        self.assertFalse(GithubOrgClient.has_license(repo_without_license, "MIT"))
        with self.assertRaises(AssertionError):
            GithubOrgClient.has_license(repo_with_license, None)


if __name__ == '__main__':
    unittest.main()