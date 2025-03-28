# src/fetch_github.py

import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

def get_repo_details(repo_url):
    """
    Fetch README content, stats, contributors, and file list for a GitHub repository.
    
    Args:
        repo_url (str): GitHub repository URL (e.g., https://github.com/owner/repo)
    
    Returns:
        tuple: (readme_text, stats, contributors, file_list)
    """
    if not GITHUB_API_KEY:
        raise ValueError("GITHUB_API_KEY not found in environment variables.")

    try:
        parts = repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        if not owner or not repo:
            raise ValueError("Invalid repository URL format.")
    except IndexError:
        return "Invalid URL: Could not parse owner/repo.", {}, [], []

    headers = {"Authorization": f"token {GITHUB_API_KEY}", "Accept": "application/vnd.github.v3+json"}

    # Fetch README
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        readme_res = requests.get(readme_url, headers=headers, timeout=10)
        if readme_res.status_code == 200:
            readme_data = readme_res.json()
            readme_text = base64.b64decode(readme_data.get("content", "")).decode("utf-8")
        else:
            readme_text = f"README not found (Status: {readme_res.status_code})."
    except requests.RequestException as e:
        readme_text = f"Error fetching README: {str(e)}"

    # Fetch Repo Stats
    repo_url_api = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        repo_res = requests.get(repo_url_api, headers=headers, timeout=10)
        if repo_res.status_code == 200:
            repo_data = repo_res.json()
            stats = {
                "Stars": repo_data.get("stargazers_count", 0),
                "Forks": repo_data.get("forks_count", 0),
                "Watchers": repo_data.get("watchers_count", 0),
            }
        else:
            stats = {"Stars": 0, "Forks": 0, "Watchers": 0}
    except requests.RequestException:
        stats = {"Stars": 0, "Forks": 0, "Watchers": 0}

    # Fetch Contributors
    contributors_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    try:
        contributors_res = requests.get(contributors_url, headers=headers, timeout=10)
        if contributors_res.status_code == 200 and isinstance(contributors_res.json(), list):
            contributors = [c["login"] for c in contributors_res.json()[:5]]
        else:
            contributors = []
    except requests.RequestException:
        contributors = []

    # Fetch File List
    file_list = get_repo_files(owner, repo, headers)

    return readme_text, stats, contributors, file_list

def get_repo_files(owner, repo, headers):
    """
    Fetch all file names from the repository's default branch.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        headers (dict): Authorization headers
    
    Returns:
        list: List of file paths
    """
    # First, get the default branch
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        repo_res = requests.get(repo_url, headers=headers, timeout=10)
        if repo_res.status_code != 200:
            return []
        default_branch = repo_res.json().get("default_branch", "main")
    except requests.RequestException:
        return []

    # Fetch the tree from the default branch
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    try:
        tree_res = requests.get(tree_url, headers=headers, timeout=10)
        if tree_res.status_code == 200:
            tree_data = tree_res.json()
            # Extract file paths (exclude directories)
            file_list = [item["path"] for item in tree_data.get("tree", []) if item["type"] == "blob"]
            return file_list
        else:
            return []
    except requests.RequestException:
        return []

# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/python/cpython"
    readme, stats, contributors, files = get_repo_details(repo_url)
    print("README:", readme[:200])
    print("Stats:", stats)
    print("Contributors:", contributors)
    print("Files:", files[:10])  # Print first 10 files for brevity