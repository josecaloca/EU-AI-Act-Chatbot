from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import streamlit as st


#Return vectorstore for the PDF_path
def get_vector_store(pdf_files):
    all_chunks = []
    
    for pdf_file in pdf_files:
        # Load the PDF content
        loader = PyPDFLoader(pdf_file)
        data = loader.load()

        # Define a custom text splitter with adjusted chunk size, overlap, and section-based splitting
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=450,  # Adjusted chunk size for better balance
            chunk_overlap=150,  # Adjusted overlap to ensure context retention
            separators=["\n\n", "\n", " "]  # Splitting by sections, paragraphs, and words
        )

        # Split the document into chunks and accumulate them
        chunks = text_splitter.split_documents(data)
        all_chunks.extend(chunks)

    # Create the vector store from all chunks
    vector_store = FAISS.from_documents(all_chunks, OpenAIEmbeddings(model="text-embedding-3-large"))
    return vector_store

def save_vector_store(vector_store, save_path):
    # Save the FAISS index to disk
    vector_store.save_local(save_path)
    print(f"Vector store saved at: {save_path}")
    

def load_vector_store(load_path):
    # Load the FAISS index from disk
    vector_store = FAISS.load_local(load_path, OpenAIEmbeddings(model = "text-embedding-3-large"), allow_dangerous_deserialization = True)
    print(f"Vector store loaded from: {load_path}")
    return vector_store


#Returns history_retriever_chain
def get_retreiver_chain(vector_store, 
                        temperature = 0.7, 
                        max_tokens = 1000):
    
    llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature = temperature, max_tokens = max_tokens)
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", """
        You are an expert on Artificial Intelligence and the AI-act regulation from the European Union and European policy making.
        Your goal is to make it easier for people to understand the AI-Act from the EU.

        # Make sure to:
        - Clearly state if you can't find the answer to the query. Do not try to invent an answer.
        - Focus on the differences in the text between the European Union entities: commission, council, parliament, as well as the political groups and committees.
        - Your answer must be short and concise.
        - Do not try to imagine a fake answer if you don't have the necessary information.
        """)
    ])
    history_retriver_chain = create_history_aware_retriever(llm, retriever, prompt)
    return history_retriver_chain


#Returns conversational rag
def get_conversational_rag(history_retriever_chain):
  llm=ChatOpenAI()
  answer_prompt=ChatPromptTemplate.from_messages([
      ("system","Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user","{input}")
  ])

  document_chain = create_stuff_documents_chain(llm,answer_prompt)

  #create final retrieval chain
  conversational_retrieval_chain = create_retrieval_chain(history_retriever_chain,document_chain)

  return conversational_retrieval_chain

#Returns th final response
def get_response(user_input):
  history_retriever_chain = get_retreiver_chain(st.session_state.vector_store)
  conversation_rag_chain = get_conversational_rag(history_retriever_chain)
  response = conversation_rag_chain.invoke({
        "chat_history":st.session_state.chat_history,
        "input":user_input
    })
  return response["answer"]

