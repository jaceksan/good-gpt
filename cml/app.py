import streamlit as st
from gpt import call_openapi, create_openapi_request, extract_code_block, supported_models
from slack_client import send_slack_message
from github_client import create_branch, create_pull_request, update_file_in_branch, create_file_in_branch
import os 

# define password
PASSWORD = os.environ.get("PASSWORD")

# set page config
st.set_page_config(
    layout="wide", page_icon="favicon.ico", page_title="Streamlit-GPT demo"
)

# create function to check if password is correct
def check_password(password):
    return password == PASSWORD

# ask for password
placeholder = st.empty()
password = placeholder.text_input("Enter password to access chatbot:", type="password")

# check password before allowing access to app
match check_password(password), password:
    case True, _:
        placeholder.empty()

        st.title("Chat with AI")

    supported_models = supported_models()
    model = st.selectbox(label="Models", options=supported_models, index=supported_models.index("gpt-3.5-turbo"))

    team_name = st.text_input("Enter team name:", value="Team 1")

        # Text input box
        text_input = st.text_area(
            "Enter your text here:", 
            value="""Create a Streamlit app:
            1. Input box (area) for larger texts
            2. Call ChatGPT, send the text from the input box.
            3. Display the result from the ChatGPT"""
        )

        if 'final_code' not in st.session_state:
            st.session_state.final_code = ""

        # Button to send text to OpenAI
        if st.button("Generate code"):
            print(f"{text_input=}")
            markdown_response = call_openapi(create_openapi_request(text_input), model)
            final_code = extract_code_block(markdown_response)
            st.session_state.final_code = markdown_response

        st.markdown(st.session_state.final_code, unsafe_allow_html=True)

        if st.session_state.final_code and st.button("Send result to Slack"):
            send_slack_message(
                f"Input: {text_input}\n{st.session_state.final_code}"
            )
    if st.session_state.final_code and st.button("Create Pull Request"):
        create_branch(team_name)
        create_file_in_branch(file_name=f"{team_name}/app.py",file_content=st.session_state.final_code,commit_message="{team_name}-kickoff", branch_name=team_name)
        create_pull_request(f"{team_name} kickoff", f"{team_name} kickoff:\nSpecification:\n{text_input}", team_name, 'main')
    
    case False, "":
        pass
    case False, _:
        st.write("Incorrect password.")
