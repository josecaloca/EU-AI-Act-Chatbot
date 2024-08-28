from langchain_core.messages import HumanMessage, AIMessage
import os
import streamlit as st
from src.helper_functions import get_vector_store, save_vector_store, load_vector_store, get_response

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

#Streamlit app

st.header("EU AI Act chatbot")

chat_history=[]
vector_store=[]

#session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi I'm EuroX, how can I help you?")
    ]

if vector_store not in st.session_state:
    vector_store_folder = "./vector_store"
    
    if os.path.exists(vector_store_folder):
        # If the folder exists, load the vector store from the folder
        st.session_state.vector_store = load_vector_store(vector_store_folder)
    else:
        # If the folder doesn't exist, create and save the vector store
        data_folder = "./data"
        pdf_files = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.pdf')]
        
        st.session_state.vector_store = get_vector_store(pdf_files)
        save_vector_store(vector_store, vector_store_folder)
        
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
