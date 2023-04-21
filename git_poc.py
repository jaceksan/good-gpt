from github_client import *

if __name__ == "__main__":
    # Create a new branch
    new_branch = create_branch('test-branch')
    print(new_branch)

    # Commit to the new branch
    commit_to_branch('test-branch', 'README.md', 'Commit to test branch')

    # Create a pull request
    pull_request = create_pull_request('Test Pull Request', 'This is a test pull request', 'test-branch', 'main')
    print(pull_request)