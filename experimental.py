'''
This file is experimental file 
for also enabling the option of RAG as well
'''

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
loader=None
all_text=""
if uploaded_file:
    reader=PdfReader(uploaded_file)
    for page in reader.pages:
                all_text+=page.extract_text()
if all_text !="":
    text_splitter = CharacterTextSplitter(separator='\n',chunk_size=500,chunk_overlap=150,length_function=len)
    documents = text_splitter.create_documents(all_text)
    st.write(len(documents))
    st.write(documents[0])
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(documents, embeddings)
    question = st.text_area("Your text")
    if question:
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversational_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(), memory=memory)
        answer = conversational_chain.invoke({'question':question})
    
        st.write(answer['answer'])
