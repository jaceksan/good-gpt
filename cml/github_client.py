import os
from dataclasses import dataclass

from github import Github
from dotenv import load_dotenv

load_dotenv()


def create_branch(branch_name: str):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

    # Set user, repo, branch and file path
    user = os.environ['GITHUB_REPO_OWNER']
    repo = os.environ['GITHUB_REPO_NAME']
    base_branch_default = 'main'

    # Get repository
    repo = g.get_user(user).get_repo(repo)

    print(repo)
    # Retrieve base branch
    base_branch = repo.get_branch(base_branch_default)

    # Create new branch
    new_branch = repo.create_git_ref(ref='refs/heads/' + branch_name, sha=base_branch.commit.sha)

    return new_branch


def create_pull_request(title: str, body: str, head_branch: str, base_branch: str = 'main'):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

    # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']

    # Get repository
    repo = g.get_user(user).get_repo(repo_name)

    # Create a new pull request
    pull_request = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)

    return pull_request


def update_file_in_branch(branch_name, file_path, updated_content, commit_message):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

    # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']

    # Get repository and branch
    repo = g.get_user(user).get_repo(repo_name)
    branch = repo.get_branch(branch_name)

    # Get file contents and update it
    file = repo.get_contents(file_path, ref=branch_name)
    file_content = file.decoded_content.decode('utf-8')
    # updated_content = file_content + '\nSome changes.'

    # Create a new commit with updated file

    repo.update_file(file_path, commit_message, updated_content, file.sha, branch=branch_name)

    return "Changes committed to branch: " + branch_name


def create_file_in_branch(file_name: str, file_content: str, commit_message: str, branch_name: str):
    # create a Github object using the provided access token
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

    # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']

    # Get repository and branch
    repo = g.get_user(user).get_repo(repo_name)

    # create a new file
    repo.create_file(file_name, commit_message, file_content, branch=branch_name)


def read_pull_request_comments(pr_number):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])  # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']

    # Get repository and pull request
    repo = g.get_user(user).get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Get all comments
    comments = pr.get_review_comments()
    comments_list = []

    # Loop through comments and append to list
    for comment in comments:
        comments_list.append(comment)

    return comments_list


@dataclass
class PullRequest:
    title: str
    pr_number: str
    state: str
    branch_name: str
    login: str

    @classmethod
    def from_pull(cls, pull):
        """
        :param pull: PullRequest
        """
        return cls(pull.title, pull.number, pull.state, pull.head.ref, pull.user.login)


def list_pull_requests() -> list[PullRequest]:
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])  # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']

    # Get repository and pull request
    repo = g.get_user(user).get_repo(repo_name)

    pulls = repo.get_pulls()
    result = []
    for pull in pulls:
        result.append(PullRequest.from_pull(pull))
    return result
