from gpt_util import call_openapi, extract_code_block
from git_client import GithubClient
from git_utils import PullReq, branch_to_file_path
from dotenv import load_dotenv
import sys

load_dotenv()   

class PrUpdateAgent:
    """Summary: Agent, that updates the the GoodGPT created Pull Request based on reviews
    """
    gitClient : GithubClient = GithubClient()
    system_message = "You are a Python expert at working with Streamlit. You create small-scale Streamlit applications. You never write anything else than code."
    model_engine="gpt-4-0314"

    def __init__(self, model_engine: str = "gpt-4-0314") -> None:
        self.model_engine = model_engine

    @classmethod
    def fetch_file_contents(self, pr: PullReq):
        code_context = ""
        for file_path in pr.file_paths:
            code_context += f"File: {file_path.filename} content: { self.gitClient.get_file_content(pr.branch_name,file_path.filename) }\n "
        return code_context

    @classmethod
    def parse_pr_comments(self, pr_reviews: list):
        parsed_reviews = "Please make changes according to: \n"
        for review in pr_reviews:
            parsed_reviews += review.body + "\n"
            if len(review.comments) > 0:
                parsed_reviews += "With more specific comments: \n"
                for comment in review.comments:
                    parsed_reviews += f"At line {comment.original_line}: {comment.body} \n"
        return parsed_reviews
            

    @classmethod
    def create_redo_request(self, content: str, code_context: str, pr_reviews: list) -> list:
        return [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": content
            },
            {
                "role": "assistant",
                "content": code_context
            },
            {
                "role": "user",
                "content": self.parse_pr_comments(pr_reviews)
            }
        ]

    @classmethod
    def resolve_reviews(self, pr: PullReq, comments):
        updated_content=extract_code_block(
            call_openapi(
            self.create_redo_request(
                content=pr.body,
                code_context=self.fetch_file_contents(pr),
                pr_reviews=pr.reviews
            ),
            model_engine=self.model_engine,
            )
        )
        print(updated_content)
        self.gitClient.set_branch(pr.branch_name)
        self.gitClient.update_file_in_branch(
            file_path=branch_to_file_path(pr.branch_name),
            updated_content=updated_content,
            commit_message="Resolving PR comments"
        )
   

    def check_reviews(self, pr_number: int):
        if self.gitClient.get_raw_pull_request(pr_number).get_reviews().totalCount > 0:
            for review in self.gitClient.get_pull_request(pr_number).reviews:
                if review.status == "CHANGES_REQUESTED":
                    self.resolve_reviews(self.gitClient.get_pull_request(pr_number), review)


    def check_pull_requests(self):
        return NotImplemented



if __name__ == "__main__":
    if len(sys.argv) > 1:
        pr_number = int(sys.argv[1])
    else:
        raise ValueError("Please provide a pull request number")

    pr_update_agent = PrUpdateAgent()
    pr_update_agent.check_reviews(pr_number)