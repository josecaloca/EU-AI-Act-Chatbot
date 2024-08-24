from langchain_core.messages import HumanMessage, AIMessage
import os
import streamlit as st
from src.helper_functions import get_vector_store, get_response

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]




#Streamlit app

st.header("Chat with websites")

chat_history=[]
vector_store=[]


# Sidebar
# URL pasting in sidebar on the left
with st.sidebar:
  st.header("Paste your URL")
  website_url = st.text_input("Enter URL")

if website_url is None or website_url.strip()=="":
  st.info("Please enter a website URL")
else:
  #session state
  if "chat_history" not in st.session_state:
    st.session_state.chat_history=[
        AIMessage(content="I am a bot, how can I help you?")
    ]
   #create conversation chain
  if vector_store not in st.session_state:
      st.session_state.vector_store = get_vector_store(website_url)

  user_input=st.chat_input("Type your message here...")
  if user_input is not None and user_input.strip()!="":
    response = get_response(user_input)

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response))

  for message in st.session_state.chat_history:
      if isinstance(message,AIMessage):
        with st.chat_message("AI"):
          st.write(message.content)
      else:
        with st.chat_message("Human"):
          st.write(message.content)





