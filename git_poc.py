from github_client import *

if __name__ == "__main__":

    branch_name="test-branch5"
    commit_message="Test commit V2.1"
    update_commit_message="Test commit V2.2"
    file_name="new_awesome_file.txt"
    file_content="Some random sample content\nThis is a second line\nThis is a third line"
    updated_file_content=file_content+"\nThis is a fourth line"
    # Create a new branch
    new_branch = create_branch(branch_name)
    #print(new_branch)

    # Commit to the new branch
    create_file_in_branch(file_name=file_name,file_content=file_content,commit_message=update_commit_message, branch_name=branch_name)

    update_file_in_branch(branch_name=branch_name, file_path=file_name, updated_content=updated_file_content, commit_message=commit_message)

    # Create a pull request
    pull_request = create_pull_request('Test Pull Request V1.2', 'This is a test pull request V1.2', branch_name, 'main')
    print(pull_request)