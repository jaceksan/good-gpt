from gpt_util import call_openapi, extract_code_block
from git_client import GithubClient
from git_utils import PullReq, branch_to_file_path
from dotenv import load_dotenv
import sys

load_dotenv()   

class PrReviewAgent:
    """Summary: Class for PR review agent
    """
    gitClient : GithubClient = GithubClient()
    
    system_message = "You are a Python expert. Your specialiazation is at reviewing Pull Requests. You review code, but also code contentions. Your responses always start with \"GoodGPT Automatic Code Review:\" and one of the following: (\"APPROVE\",\"REQUEST CHANGES\",\"NEED MORE INFORMATION\" or \"UNSURE\"). Then followed by your review."
 
    model_engine="gpt-4-0314"

    def __init__(self, model_engine: str = "gpt-4-0314") -> None:
        self.model_engine = model_engine

    @classmethod
    def fetch_file_contents(self, pr: PullReq):
        code_context = ""
        for file in pr.files:
            if file.status == "added":
                code_context += f"Added file:\n-{file.filename}\nContent:\n{ self.gitClient.get_file_content(pr.branch_name,file.filename) }\n"
            if file.status == "modified":
                code_context += f"Modified file:\n-{file.filename}\nContent:\n{ self.gitClient.get_file_content(pr.branch_name,file.filename) } Diff:\n{ file.patch }\n"
            if file.status == "removed":
                code_context += f"Removed file:\n-{file.filename}\nDiff:\n{ file.patch }\n"
        return code_context


    @classmethod
    def construct_pr_review_request(self, pr: PullReq):
        """Summary: Construct the request for the Pull Request review
        """
        request = "Please provide a review for this Pull Request. \nThe files are as follows: \n"
        request += self.fetch_file_contents(pr)
        return request


    @classmethod
    def create_redo_request(self, pr: PullReq) -> list:
        return [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": self.construct_pr_review_request(pr)
            }
        ]

    @classmethod
    def resolve_review(self, gpt_comment):
        """Summary: Resolve the Pull Request based on the comments
        """
        if "REQUEST CHANGES" in gpt_comment:
            return 'REQUEST_CHANGES'
        if "APPROVE" in gpt_comment:
            return 'APPROVE'
        return 'COMMENT'

    @classmethod
    def check_pull_request(self, pr_number: int):
        """Summary: Resolve the Pull Request based on the comments
        """
        pr = self.gitClient.get_pull_request(pr_number)
        gpt_comment = call_openapi(
            self.create_redo_request(pr),
            model_engine=self.model_engine
        )
        self.gitClient.add_pr_review(pr_number, gpt_comment, self.resolve_review(gpt_comment))
        

        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        pr_number = int(sys.argv[1])
    else:
        raise ValueError("Please provide a pull request number")

    pr_update_agent = PrReviewAgent()
    pr_update_agent.check_pull_request(pr_number)