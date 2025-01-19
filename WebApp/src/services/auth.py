import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from src.utils.settings import (
    GITHUB_AUTHORIZATION_BASE_URL,
    GITHUB_TOKEN_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
)

# Initialize OAuth2 session
oauth = OAuth2Session(
    GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, redirect_uri=GITHUB_REDIRECT_URI
)


def authenticate_with_github():
    """
    Starts the GitHub OAuth login flow.
    This function generates the authorization URL and handles the OAuth response.
    """
    authorization_url, state = oauth.create_authorization_url(
        GITHUB_AUTHORIZATION_BASE_URL
    )

    # Customizing the page with GitHub's logo and modern layout
    st.markdown(
        """
        <style>
            .title {
                font-size: 40px;
                font-weight: bold;
                color: #24292f;
                text-align: center;
                margin-top: 50px;
            }
            .description {
                font-size: 18px;
                color: #586069;
                text-align: center;
            }
            .auth-button {
                display: inline-block;
                background-color: #0366d6;
                color: white;
                padding: 15px 30px;
                border-radius: 5px;
                text-decoration: none;
                font-size: 18px;
                text-align: center;
                margin-top: 20px;
                width: auto;
                transition: background-color 0.3s;
            }
            .auth-button:hover {
                background-color: #0056b3;
            }
            .container {
                text-align: center;
                padding: 20px;
            }
            .github-logo {
                width: 30px;
                vertical-align: middle;
                margin-right: 10px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="title">Please authenticate to use the app</div>',
        unsafe_allow_html=True,
    )

    # Add GitHub logo and link styled as a button
    st.markdown(
        """
        <div class="container">
            <p class="description">
                Please go to this URL to authorize the app: 
            </p>
            <a class="auth-button" href="{}" target="_blank">
                <img class="github-logo" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub Logo">
                Authorize with GitHub
            </a>
        </div>
    """.format(
            authorization_url
        ),
        unsafe_allow_html=True,
    )


def handle_github_callback():
    """
    Handles the GitHub callback after user authorizes the app and returns the access token.
    Automatically extracts the code from the callback URL and exchanges it for the access token.
    """
    params = st.query_params  # Use st.query_params to get query parameters
    code = params.get("code", None)

    if code:
        # If the 'code' parameter exists, we exchange it for the token
        token = oauth.fetch_token(
            GITHUB_TOKEN_URL,
            authorization_response=f"{GITHUB_REDIRECT_URI}?code={code}",
        )
        st.session_state["github_token"] = token
        st.session_state["is_authenticated"] = True
        st.rerun()  # Trigger a rerun to refresh the page and show the real content


def display_authenticated_content():
    """
    Displays the authenticated user's content after successful GitHub authentication.
    This function will only show the main app content, not the user's GitHub profile.
    """
    if "is_authenticated" in st.session_state and st.session_state["is_authenticated"]:
        st.sidebar.write("You are logged in with GitHub!")
        st.sidebar.write(
            "Proceed to interact with the ChatGPT model."
        )  # Instead of showing GitHub profile
    else:
        authenticate_with_github()


def check_authentication():
    """
    Checks if the user is authenticated.
    Returns True if authenticated, else False.
    """
    return (
        "is_authenticated" in st.session_state and st.session_state["is_authenticated"]
    )
