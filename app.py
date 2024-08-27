from langchain_core.messages import HumanMessage, AIMessage
import os
import streamlit as st
from src.helper_functions import get_vector_store, get_response

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]



#Streamlit app

<<<<<<< HEAD
st.header("EU AI Act chatbot")
=======
st.header("EU AI Act info")
>>>>>>> 23b3e95c0cb927a8600de0f82ec89a6d4c835dd7

chat_history=[]
vector_store=[]

<<<<<<< HEAD
#session state
if "chat_history" not in st.session_state:
  st.session_state.chat_history=[
      AIMessage(content="I am a bot, how can I help you?")
  ]
 #create conversation chain
if vector_store not in st.session_state:
    PDF_path = "./data/EU_AI_Act_June_2024.pdf"
    st.session_state.vector_store = get_vector_store(PDF_path)
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
=======
# Message container
if "chat_history" not in st.session_state:
  st.session_state.chat_history = [
    AIMessage(content="Ask me anything about the new EU AI Act!")
  ]
# create conversation chain
if vector_store not in st.session_state:
  st.session_state.vector_store = get_vector_store("./data/EU_AI_Act_June_2024.pdf")

st.write("Ask me anything about the new EU AI Act!")
user_input = st.chat_input("Type your message here...")
if user_input is not None and user_input.strip() != "":
  response = get_response(user_input)

  st.session_state.chat_history.append(HumanMessage(content=user_input))
  st.session_state.chat_history.append(AIMessage(content=response))

for message in st.session_state.chat_history:
  if isinstance(message, AIMessage):
    with st.chat_message("AI"):
      st.write(message.content)
  else:
    with st.chat_message("Human"):
      st.write(message.content)






>>>>>>> 23b3e95c0cb927a8600de0f82ec89a6d4c835dd7
