import streamlit as st
from gpt import call_openapi, create_openapi_request, extract_code_block, supported_models
from slack_client import send_slack_message
from github_client import GithubClient, GPT_USER
import os 
import re
import yaml

# define password
PASSWORD = os.environ.get("PASSWORD")
EXAMPLES_DIR = pathlib.Path(__name__).parent / "examples"


# create function to check if password is correct
def check_password(password):
    return password == PASSWORD


def project_for_branch(branch_name: str):
    return branch_name.removeprefix(f"{GPT_USER}/")


def handle_project_name(github_client):
    if "project_name" not in st.session_state:
        st.session_state.project_name = None

    existing_projects = [project_for_branch(b) for b in github_client.list_gpt_branches()]
    project_name = st.sidebar.text_input("Enter project name:")
    project_branch_name = re.sub('[^a-zA-Z0-9_]+', '_', project_name) if isinstance(project_name, str) else project_name
    if project_name and project_name not in existing_projects:
        if st.sidebar.button("Create project"):
            github_client.set_branch(project_branch_name)
            github_client.create_branch()
            existing_projects.append(project_branch_name)
            st.session_state.project_name = project_branch_name

    st.session_state.project_name = st.sidebar.selectbox(
        label="Projects",
        options=existing_projects,
        index=existing_projects.index(st.session_state.project_name) if st.session_state.project_name else 0
    )
    project_branch_name = re.sub('[^a-zA-Z0-9_]+', '_', st.session_state.project_name) if isinstance(st.session_state.project_name, str) else project_name
    github_client.set_branch(project_branch_name)


def read_examples() -> dict[str, dict]:
    file_dict = {}
    for filename in os.listdir(EXAMPLES_DIR):
        # Check if the file is a regular file (i.e. not a directory)
        if os.path.isfile(os.path.join(EXAMPLES_DIR, filename)):
            # Open the file and read its contents
            with open(os.path.join(EXAMPLES_DIR, filename), "r") as file:
                content = file.read()
                # Store the YAML content in the dictionary indexed by the file name
                parsed_content = yaml.safe_load(content)
                file_dict[filename] = parsed_content
    return file_dict


def app():
    st.title("Design Streamlit apps with ChatGPT")

    models = supported_models()
    model = st.sidebar.selectbox(label="OpenAI models", options=models, index=models.index("gpt-3.5-turbo"))
    github_client = GithubClient()

    handle_project_name(github_client)

    examples = read_examples()
    example = st.sidebar.selectbox("Examples", options=examples.keys())
    # Text input box
    text_input = st.text_area("Enter your text here", value=examples[example]["design"])

    if 'final_code' not in st.session_state:
        st.session_state.final_code = ""
    if 'markdown_code' not in st.session_state:
        st.session_state.markdown_code = ""

    # Button to send text to OpenAI
    if st.button("Generate code"):
        st.session_state.markdown_code = call_openapi(create_openapi_request(text_input), model)
        st.session_state.final_code = extract_code_block(st.session_state.markdown_code)

    st.markdown(st.session_state.markdown_code, unsafe_allow_html=True)

    if st.session_state.final_code and st.button("Send result to Slack"):
        send_slack_message(
            f"Input: {text_input}\n{st.session_state.final_code}"
        )
    if st.session_state.final_code and st.button("Create Pull Request"):
        github_client.handle_pull_request(st.session_state.project_name, text_input)


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
