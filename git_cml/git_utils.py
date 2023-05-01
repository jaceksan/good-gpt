import requests
from dataclasses import dataclass
from github import PullRequest
from gpt_util import GPT_USER

@dataclass
class ReviewComment:
    body: str
    user: str
    original_line: int
    line: int
    file_path: str
    diff: str

@dataclass
class Review:
    body: str
    user: str
    status: str
    comments: list[ReviewComment]


@dataclass
class PullReq:
    title: str
    pr_number: str
    state: str
    branch_name: str
    login: str
    body: str
    diff: str
    reviews: list[Review]
    files: list[str]

    @classmethod
    def parse_reviews(cls, pr):
        """Summary: Parse comments from Github PullReq object

        Args:
            comments (list): List of Github PullReq comments

        Returns:
            list(ReviewComment): List of ReviewComment objects
        """
        reviews = []
        pr_reviews = pr.get_reviews()
        for rev in pr_reviews:
            review = Review(
                body=rev.body,
                user=rev.raw_data['user']['login'],
                status=rev.state,
                comments= []
            )
            for cmt in pr.get_review_comments():
                if rev.id == cmt.raw_data['pull_request_review_id']:
                    review.comments.append(
                        ReviewComment(
                            body=cmt.raw_data['body'],
                            user=cmt.raw_data['user']['login'],
                            original_line=cmt.raw_data['line'],
                            line=cmt.raw_data['line'],
                            file_path=cmt.path,
                            diff=cmt.diff_hunk
                        )
                    )
                    
            reviews.append(review)
        return reviews

    @classmethod
    def from_pull(cls, pull: PullRequest.PullRequest):
        """Summary: Create PullReq object from a Github PullReq object

        Args:
            pull (): Github PullReq object

        Returns:
            PullReq: PullReq object
        """
        return cls(
            pull.title,
            pull.number,
            pull.state,
            pull.head.ref,
            pull.user.login,
            pull.body,
            requests.get(pull.diff_url).text,
            cls.parse_reviews(pull),
            pull.get_files()
        )

def branch_to_file_path(branch_name: str):
    return "apps/" + branch_name.removeprefix(f"{GPT_USER}/") + "/app.py"