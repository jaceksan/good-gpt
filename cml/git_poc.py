from github_client import *

if __name__ == "__main__":


    branch_name = "Team-1234"
    pr = get_pull_request(branch_name=branch_name)
    print(pr)
    comments = list_pull_request_comments(branch_name=branch_name)
    print(comments)
    print(get_pull_request_url(branch_name=branch_name))