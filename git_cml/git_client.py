import os
from github import Github
from dotenv import load_dotenv
from git_utils import PullReq
import streamlit as st
from gpt_util import GPT_USER, APPS_FOLDER

load_dotenv()

class GithubClient:
    def __init__(self):
        # Authentication
        self.g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

        # Set user, repo, branch and file path
        self.user = os.environ['GITHUB_REPO_OWNER']
        self.repo_name = os.environ['GITHUB_REPO_NAME']
        self.base_branch_default = 'main'
        # Get repository
        self.repo = self.g.get_user(self.user).get_repo(self.repo_name)

        self.project_name = None
        self.branch_name = None

    def set_project(self, project_name: str) -> None:
        """Summary: Set project name

        Args:
            project_name (str): Project name
        """
        self.project_name = project_name
        self.branch_name = f"{GPT_USER}/{self.project_name}"

    def set_branch(self, branch_name: str) -> None:
        """Summary: Set branch name

        Args:
            branch_name (str): Branch name
        """
        self.branch_name = branch_name

    def create_branch(self):
        # Retrieve base branch
        base_branch = self.repo.get_branch(self.base_branch_default)

        # Create new branch
        new_branch = self.repo.create_git_ref(
            ref=f"refs/heads/{self.branch_name}",
            sha=base_branch.commit.sha
        )

        return new_branch

    def get_pull_request(self, pr_number):
        """Summary: Get pull request

        Args:
            pr_number (_type_): Pull Request number

        Returns:
            PullReq: PullReq object
        """
        return PullReq.from_pull(self.repo.get_pull(pr_number))

    def get_raw_pull_request(self, pr_number):
        """Summary: Get raw pull request

        Args:
            pr_number (_type_): Pull Request number

        Returns:
            PullReq: PullReq object
        """
        return self.repo.get_pull(pr_number)

    def list_gpt_branches(self):
        """Summary: List all branches that start with 'GPT_USER'

        Returns:
            list(Branch)
        """
        branches = self.repo.get_branches()
        return [b.name for b in branches if b.name.startswith(f"{GPT_USER}/")]

    def list_non_gpt_pr(self):
        """Summary: List all open pull requests that do not start with 'GPT_USER'

        Returns:
            list(PullReq)
        """
        pulls = self.repo.get_pulls(state='open')
        return [PullReq.from_pull(p) for p in pulls if not p.head.ref.startswith(f"{GPT_USER}/")]
    
    def list_gpt_unresolved_pr(self):
        """Summary: List all open pull requests that start with 'GPT_USER' and are not approved

        Returns:
            list(PullReq)
        """
        pulls = self.repo.get_pulls(state='request_changes')
        return [PullReq.from_pull(p) for p in pulls if p.head.ref.startswith(f"{GPT_USER}/")]

    def create_pull_request(self, title: str, body: str, base_branch: str = 'main'):
        """Summary: Create a pull request

        Args:
            title (str): Pull request title
            body (str): Pull request body
            base_branch (str, optional): Base branch. Defaults to 'main'.

        Returns:
            PullReq
        """
        # Create a new pull request
        pull_request = self.repo.create_pull(title=title, body=body, head=self.branch_name, base=base_branch)
        return pull_request
    
    def update_file_in_branch(self, file_path, updated_content, commit_message):
        """Summary: Update a file in a branch

        Args:
            file_path (_type_): File path
            updated_content (_type_): Updated file content
            commit_message (_type_): Commit message

        Returns:
            str: Commit message
        """
        file= self.repo.get_contents(file_path, ref=self.branch_name)

        self.repo.update_file(file_path, commit_message, updated_content, file.sha, branch=self.branch_name)

        return "Changes committed to branch: " + self.branch_name

    def create_file_in_branch(self, file_name: str, file_content: str, commit_message: str):
        """Summary: Create a file in a branch

        Args:
            file_name (str): File Name
            file_content (str): File content
            commit_message (str): Commit message

        Returns:
            None
        """
        # create a Github object using the provided access token
        # create a new file
        self.repo.create_file(file_name, commit_message, file_content, branch=self.branch_name)


    def get_file_content(self, branch_name, file_path):
        """Summary: Get the content of a file in a branch

        Args:
            branch_name (_type_): Branch name
            file_path (_type_): File path

        Returns:
            str: File content
        """
        # Get the branch object
        branch = self.repo.get_branch(branch_name)
        
        # Get the file's content from the branch
        file_content = self.repo.get_contents(file_path, ref=branch.commit.sha)
        
        # Decode the file content
        decoded_content = file_content.decoded_content.decode()
        
        return decoded_content

    def get_pull_request_comments(self, pr_number):
        """Summary: Read all comments in a pull request

        Args:
            pr_number (_type_): Pull request number

        Returns:
            list(Comment): List of comments
        """
        return self.repo.get_pull(pr_number)

    def list_pull_requests(self) -> list[PullReq]:
        """Summary: List all pull requests

        Returns:
            list[PullReq]: List of pull requests
        """
        pulls = self.repo.get_pulls()
        result = []
        for pull in pulls:
            result.append(PullReq.from_pull(pull))
        return result

    def list_gpt_pull_requests(self) -> list[PullReq]:
        return [p for p in self.list_pull_requests() if p.login == GPT_USER]

    def list_existing_apps(self) -> list[str]:
        """Summary: List all existing apps

        Returns:
            list[str]: List of app names
        """
        try:
            contents = self.repo.get_contents(APPS_FOLDER)
            return [c.name for c in contents if c.type == "dir"]
        except Exception:  # noqa
            return []

    def handle_pull_request(self, project_name, text_input):
        """Summary: Handle a pull request

        Args:
            project_name (str): Project name
            text_input (str): Text input
        
        Returns:
            None
        """
        self.create_file_in_branch(
            file_name=f"{APPS_FOLDER}/{project_name}/app.py",
            file_content=st.session_state.final_code,
            commit_message=f"{project_name}-kickoff",
        )
#         requirements_content = """streamlit
# pandas
# altair
# """
#         self.create_file_in_branch(
#             file_name=f"{APPS_FOLDER}/{project_name}/requirements.txt",
#             file_content=requirements_content,
#             commit_message=f"{project_name}-requirements",
#         )
        self.create_pull_request(
            title=f"{project_name} kickoff",
            body=f"{project_name} kickoff:\nSpecification:\n{text_input}",
            base_branch='main'
        )

    def project_states(self) -> tuple[bool, bool]:
        """Summary: Get the states of a project
        
        Returns:
            tuple[bool, bool]: Existing app, Opened pull request
        """

        existing_app = False
        opened_pr = False

        # existing app
        existing_projects = self.list_existing_apps()
        for project in existing_projects:
            if project == self.project_name:
                existing_app = True
                break

        # opened pull request
        gpt_opened_pull_requests = self.list_gpt_pull_requests()
        for pr in gpt_opened_pull_requests:
            if pr.branch_name == self.branch_name:
                opened_pr = True
                break

        return existing_app, opened_pr

    def add_pr_review(self, pr_number, comment, status):
        """Summary: Add a review to a pull request

        Args:
            pr_number (_type_): Pull request number
            comment (_type_): Comment
            status (_type_): Status

        Returns:
            None
        """
        self.repo.get_pull(pr_number).create_review(body=comment, event=status)
        