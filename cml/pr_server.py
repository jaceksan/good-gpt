from github_client import GithubClient, GPT_USER
from gpt import create_openapi_request, call_openapi, extract_code_block, create_openapi_redo_request

def branch_to_file_path(branch_name: str):
    return "apps/" + branch_name.removeprefix(f"{GPT_USER}/") + "/app.py"

def resolve_comment(pr, comment):
    
    gitclient = GithubClient()

    # Resolve comment
    
    updated_content = extract_code_block(
        call_openapi(
            create_openapi_redo_request(
                content=pr.body,
                code_context= gitclient.get_file_content(
                    pr.head.ref,
                    branch_to_file_path(pr.head.ref)
                ),
                pr_comment=comment.body
            ),
            model_engine="gpt-3.5-turbo"
        )
    )

    gitclient.update_file_in_branch(
        file_path=branch_to_file_path(pr.head.ref),
        updated_content=updated_content,
        commit_message="Resolve comment"+comment.body
    )
   

def check_comments():
    gitclient = GithubClient()
    unresolved_pr = gitclient.list_gpt_pr_with_unresolved_comment()

    for pr in unresolved_pr:
        comment = gitclient.get_unresolved_comments(pr) # For now there is only one comment, but in the future there could be multiple comments
        resolve_comment(pr, comment) # in future, let's resolve all comments together


def check_pull_requests():
    return NotImplemented


if __name__ == "__main__":
    check_comments()
    check_pull_requests()
