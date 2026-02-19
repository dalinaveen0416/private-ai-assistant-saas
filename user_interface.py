import streamlit as st
import requests

# CONFIG
API_URL = "http://127.0.0.1:9000"


st.set_page_config(
    page_title="Private AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# STYLE

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 6rem;
}

.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background-color: #2b313e;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}

.ai-msg {
    background-color: #444654;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 25%;
    width: 50%;
}

</style>
""", unsafe_allow_html=True)

# SESSION STATE

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# API FUNCTIONS

def register(email, password):
    return requests.post(
        f"{API_URL}/register",
        params={"email": email, "password": password}
    )

def login(email, password):
    return requests.post(
        f"{API_URL}/login",
        params={"email": email, "password": password}
    )

def upload_file(file):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    return requests.post(
        f"{API_URL}/upload",
        headers=headers,
        files={"file": file}
    )

def ask_question(query):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    return requests.post(
        f"{API_URL}/chat",
        headers=headers,
        params={"query": query}
    )

def get_history():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    return requests.get(
        f"{API_URL}/history",
        headers=headers
    )
#LOGIN / REGISTER

if st.session_state.token is None:

    st.markdown("<h1 style='text-align: center;'>🤖 Private AI Assistant</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):

                res = login(email, password)

                if res.status_code == 200:

                    st.session_state.token = res.json()["access_token"]
                    st.session_state.user = email

                    # Load last 3 chats
                    history = get_history()

                    if history.status_code == 200:

                        chats = history.json()["history"][-3:]

                        for chat in chats:

                            st.session_state.messages.append(
                                {"role": "user", "content": chat["query"]}
                            )

                            st.session_state.messages.append(
                                {"role": "assistant", "content": chat["response"]}
                            )

                    st.rerun()

                else:

                    st.error("Login failed")


        with tab2:

            email = st.text_input("Email", key="reg")
            password = st.text_input("Password", type="password", key="regp")

            if st.button("Register", use_container_width=True):

                res = register(email, password)

                if res.status_code == 200:
                    st.success("Registered successfully")
                else:
                    st.error("Registration failed")

# MAIN APP

else:

    st.sidebar.title("Private AI Assistant")
    st.sidebar.success(st.session_state.user)

    menu = st.sidebar.radio(
        "Menu",
        ["Upload Resume", "Chat", "History"]
    )

    if st.sidebar.button("Logout"):

        st.session_state.token = None
        st.session_state.user = None
        st.session_state.messages = []

        st.rerun()

    # ----- CHAT ------

    if menu == "Chat":

        st.title("Chat with your Resume")

        st.markdown('<div class="chat-container">', unsafe_allow_html=True)


        # Show only last 3 conversations
        recent_messages = st.session_state.messages[-6:]

        for msg in recent_messages:

            if msg["role"] == "user":

                st.markdown(
                    f'<div class="user-msg">🧑 {msg["content"]}</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f'<div class="ai-msg">🤖 {msg["content"]}</div>',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)


        prompt = st.chat_input("Ask anything...")

        if prompt:

            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

            with st.spinner("Thinking..."):

                res = ask_question(prompt)

                if res.status_code == 200:

                    answer = res.json()["response"]

                elif res.status_code == 400:

                    answer = "⚠️ Please upload your resume first."

                else:

                    answer = "⚠️ Something went wrong."

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            # keep only last 3 conversations
            st.session_state.messages = st.session_state.messages[-6:]

            st.rerun()


    #----- DOCM UPLOAD ------

    elif menu == "Upload Resume":

        st.title("Upload Resume")

        files = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            accept_multiple_files=True
        )

        if st.button("Upload"):

            if files:

                for file in files:

                    res = upload_file(file)

                    if res.status_code == 200:

                        st.success(f"{file.name} uploaded")

                    else:

                        st.error(f"{file.name} failed")


    # ----- STORE HISTORY -----

    elif menu == "History":

        st.title("Chat History")

        res = get_history()

        if res.status_code == 200:

            for chat in res.json()["history"]:

                st.markdown("---")

                st.write("Question:", chat["query"])
                st.write("Answer:", chat["response"])
                st.caption(chat["created_at"])

        else:

            st.error("Failed to load history")
