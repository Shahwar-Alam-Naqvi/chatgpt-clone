# 1. Import Streamlit and OpenAI
import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# openai key
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# 2. Set Title
st.title("ChatGPT Clone")

# 3. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [] # '''
                                                                # message = [
                                                                #     {"role": "user", "content": "Our Prompt"},
                                                                #     {"role": "assistant", "content": "The Response"},
                                                                #     ...
                                                                # ]
# 4. Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # model assign
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
        
# 5. React to user input.
prompt = st.chat_input("What is up ?")
if prompt:
    # display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # add message to chat history
    st.session_state.messages.append({'role': 'user', 'content':prompt})

    # display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
        