# import requests

# def fetch_commits(repo):
#     url = f"https://api.github.com/repos/{repo}/commits"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()  # Returns a list of commits
#     else:
#         print(f"Failed to fetch commits: {response.status_code}")
#         return []

# # Example usage
# repo_name = "UmarBalak/Test"  # Replace with the actual repo
# commits = fetch_commits(repo_name)
# for commit in commits:
#     print(commit['commit']['message'])

import json
import os
import requests

STATE_FILE = "last_state.json"

def fetch_commits(repo):
    url = f"https://api.github.com/repos/{repo}/commits"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def fetch_pull_requests(repo):
    url = f"https://api.github.com/repos/{repo}/pulls"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def fetch_issues(repo):
    url = f"https://api.github.com/repos/{repo}/issues"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def load_last_state():
    if os.path.exists(STATE_FILE):
        # Check if the file is non-empty
        if os.path.getsize(STATE_FILE) > 0:
            with open(STATE_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # If the JSON is invalid or corrupted, reset to default state
                    print("Corrupted state file. Resetting to default state.")
                    return {"last_commit": None, "last_pr": None, "last_issue": None}
    return {"last_commit": None, "last_pr": None, "last_issue": None}


def save_last_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def check_for_updates(repo):
    last_state = load_last_state()

    # Fetch latest commits, PRs, and issues
    commits = fetch_commits(repo)
    prs = fetch_pull_requests(repo)
    issues = fetch_issues(repo)

    # Check for new commits
    if commits:
        latest_commit = commits[0]['sha']
        if latest_commit != last_state['last_commit']:
            print(f"New commit: {commits[0]['commit']['message']}")
            last_state['last_commit'] = latest_commit

    # Check for new pull requests
    if prs:
        latest_pr = prs[0]['id']
        if latest_pr != last_state['last_pr']:
            print(f"New pull request: {prs[0]['title']}")
            last_state['last_pr'] = latest_pr

    # Check for new issues
    if issues:
        latest_issue = issues[0]['id']
        if latest_issue != last_state['last_issue']:
            print(f"New issue: {issues[0]['title']}")
            last_state['last_issue'] = latest_issue

    # Save updated state
    save_last_state(last_state)

# Example usage
repo_name = "UmarBalak/Test"  # Replace with your repository
check_for_updates(repo_name)

