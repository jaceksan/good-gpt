from asyncio import sleep
from github_client import GithubClient, GPT_USER
from gpt import create_openapi_request, call_openapi, extract_code_block, create_openapi_redo_request

def branch_to_file_path(branch_name: str):
    return "apps/" + branch_name.removeprefix(f"{GPT_USER}/") + "/app.py"

def resolve_comment(pr):
    
    gitclient = GithubClient()

    # Resolve comment
    
    updated_content = extract_code_block(
        call_openapi(
            create_openapi_redo_request(
                content=pr.body,
                code_context= gitclient.get_file_content(
                    pr.branch_name,
                    branch_to_file_path(pr.branch_name)
                ),
                pr_comment=pr.comments[0].body,
            ),
            model_engine="gpt-4-0314"
        )
    )

    gitclient.set_branch(pr.branch_name.removeprefix(f"{GPT_USER}/"))

    gitclient.update_file_in_branch(
        file_path=branch_to_file_path(pr.branch_name),
        updated_content=updated_content,
        commit_message="Resolving PR comment"
    )
   

def check_comments():
    gitclient = GithubClient()
    unresolved_pr = gitclient.list_gpt_unresolved_pr()

    for pr in unresolved_pr:
        resolve_comment(pr) # in future, let's resolve all comments together


def check_pull_requests():
    return NotImplemented


if __name__ == "__main__":
    while True:
        check_comments()
        sleep(60)
