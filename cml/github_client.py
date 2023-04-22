import os
from dataclasses import dataclass

from github import Github
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

GPT_USER = "GoodGPT"


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
        self.branch_name = None

    def set_branch(self, project_name):
        self.branch_name = f"{GPT_USER}/{project_name}"

    def create_branch(self):
        # Retrieve base branch
        base_branch = self.repo.get_branch(self.base_branch_default)

        # Create new branch
        new_branch = self.repo.create_git_ref(
            ref=f"refs/heads/{self.branch_name}",
            sha=base_branch.commit.sha
        )

        return new_branch

    def list_gpt_branches(self):
        branches = self.repo.get_branches()
        return [b.name for b in branches if b.name.startswith(f"{GPT_USER}/")]

    def create_pull_request(self, title: str, body: str, base_branch: str = 'main'):
        # Create a new pull request
        pull_request = self.repo.create_pull(title=title, body=body, head=self.branch_name, base=base_branch)
        return pull_request

    def update_file_in_branch(self, file_path, updated_content, commit_message):
        branch = self.repo.get_branch(self.branch_name)

        # Get file contents and update it
        file = self.repo.get_contents(file_path, ref=self.branch_name)
        file_content = file.decoded_content.decode('utf-8')
        # updated_content = file_content + '\nSome changes.'

        # Create a new commit with updated file

        self.repo.update_file(file_path, commit_message, updated_content, file.sha, branch=self.branch_name)

        return "Changes committed to branch: " + self.branch_name

    def create_file_in_branch(self, file_name: str, file_content: str, commit_message: str):
        # create a Github object using the provided access token
        # create a new file
        self.repo.create_file(file_name, commit_message, file_content, branch=self.branch_name)

    def read_pull_request_comments(self, pr_number):
        pr = self.repo.get_pull(pr_number)

        # Get all comments
        comments = pr.get_review_comments()
        comments_list = []

        # Loop through comments and append to list
        for comment in comments:
            comments_list.append(comment)

        return comments_list

    def list_pull_requests(self) -> list[PullRequest]:
        pulls = self.repo.get_pulls()
        result = []
        for pull in pulls:
            result.append(PullRequest.from_pull(pull))
        return result

    def list_gpt_pull_requests(self) -> list[PullRequest]:
        return [p for p in self.list_pull_requests() if p.login == GPT_USER]

    def handle_pull_request(self, project_name, text_input):
        self.create_file_in_branch(
            file_name=f"apps/{project_name}/app.py",
            file_content=st.session_state.final_code,
            commit_message=f"{project_name}-kickoff",
        )
        self.create_pull_request(
            title=f"{project_name} kickoff",
            body=f"{project_name} kickoff:\nSpecification:\n{text_input}",
            base_branch='main'
        )
