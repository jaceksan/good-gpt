import streamlit as st
from gpt import call_openapi, create_openapi_request, extract_code_block, supported_models
from slack_client import send_slack_message
from github_client import create_branch, create_pull_request, update_file_in_branch, create_file_in_branch
import os 
import re

# define password
PASSWORD = os.environ.get("PASSWORD")


# create function to check if password is correct
def check_password(password):
    return password == PASSWORD


def handle_pull_request(team_name_branch_name, team_name, text_input):
    create_branch(team_name_branch_name)
    create_file_in_branch(
        file_name=f"apps/{team_name}/app.py",
        file_content=st.session_state.final_code,
        commit_message=f"{team_name}-kickoff",
        branch_name=team_name_branch_name
    )
    create_pull_request(
        title=f"{team_name} kickoff",
        body=f"{team_name} kickoff:\nSpecification:\n{text_input}",
        head_branch=team_name_branch_name,
        base_branch='main'
    )

# reading from file
def read_file(filename):
    with open(filename, 'r') as f:
        file_contents = f.read()
    return file_contents

def app():
    st.title("Design Streamlit apps with ChatGPT")

    models = supported_models()
    model = st.sidebar.selectbox(label="OpenAI models", options=models, index=models.index("gpt-3.5-turbo"))

    team_name = st.sidebar.text_input("Enter project name:", value="Pokemon")
    team_name_branch_name = re.sub('[^a-zA-Z0-9_]+', '_', team_name)

    # Text input box
    text_input = read_file("../prompts/example1.txt")

    if 'final_code' not in st.session_state:
        st.session_state.final_code = ""
    if 'markdown_code' not in st.session_state:
        st.session_state.markdown_code = ""

    # Button to send text to OpenAI
    if st.button("Generate code"):
        st.session_state.markdown_code = call_openapi(create_openapi_request(text_input), model)
        st.session_state.final_code = extract_code_block(st.session_state.markdown_code)

    st.markdown(st.session_state.final_code, unsafe_allow_html=True)

    if st.session_state.final_code and st.button("Send result to Slack"):
        send_slack_message(
            f"Input: {text_input}\n{st.session_state.final_code}"
        )
    if st.session_state.final_code and st.button("Create Pull Request"):
        handle_pull_request(team_name_branch_name, team_name, text_input)


def main():
    # set page config
    st.set_page_config(
        layout="wide", page_icon="favicon.ico", page_title="Streamlit-GPT demo"
    )

    # ask for password
    placeholder = st.empty()
    password = placeholder.text_input("Enter password to access chatbot:", type="password")

    # check password before allowing access to app
    match check_password(password), password:
        case True, _:
            placeholder.empty()
            app()

        case False, "":
            pass
        case False, _:
            st.write("Incorrect password.")


# run the program
if __name__ == "__main__":
    main()