import os
from github import Github
from github import InputGitTreeElement
from dotenv import load_dotenv

load_dotenv()

def create_branch(branch_name):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

    # Set user, repo, branch and file path
    user = os.environ['GITHUB_REPO_OWNER']
    repo = os.environ['GITHUB_REPO_NAME']
    base_branch = 'main'

    # Get repository
    repo = g.get_user(user).get_repo(repo)

    print(repo)
    # Retrieve base branch
    base_branch = repo.get_branch(base_branch)



    # Create new branch
    new_branch = repo.create_git_ref(ref='refs/heads/' + branch_name, sha=base_branch.commit.sha)

    return new_branch

def create_pull_request(title, body, head_branch, base_branch):
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

def update_file_in_branch(branch_name, file_path, updated_content ,commit_message):
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

def create_file_in_branch(file_name:str, file_content:str, commit_message:str, branch_name:str):
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


def get_pull_request(branch_name):
    # Authentication
    g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])   # Set user and repository variables
    user = os.environ['GITHUB_REPO_OWNER']
    repo_name = os.environ['GITHUB_REPO_NAME']
    
    # Get repository and pull request
    repo = g.get_user(user).get_repo(repo_name)
    prs = repo.get_pulls()
    
    # Loop through comments and append to list
    for pr in prs:
        if pr.head.ref == branch_name:
            return pr
    
    print("No pull request found for branch: " + branch_name)
    return None

def list_pull_request_comments(branch_name):
    # Authentication
    pr = get_pull_request(branch_name)

    if pr:  
        comment_list = []
        for comment in pr.get_review_comments():
            comment_list.append(comment.body)
        return comment_list
    else:
        print("No pull request found for branch: " + branch_name)

def get_pull_request_url(branch_name):
    # Authentication
    pr = get_pull_request(branch_name)

    if pr:  
        return pr.html_url
    else:
        print("No pull request found for branch: " + branch_name)
        return None