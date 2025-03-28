import re

def extract_github_repo(url):
    match = re.search(r"github\.com/([\w-]+)/([\w-]+)", url)
    return match.groups() if match else (None, None)
