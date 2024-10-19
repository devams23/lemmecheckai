from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key not found. Please check your .env file.")
genai.configure(api_key=api_key)

# Allow dangerous deserialization (use with caution)
allow_dangerous_deserialization = True

# Function to extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks for embedding
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create FAISS vector store from text chunks
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to create the conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the question as concise and accurate as possible from the provided context. If the answer is not in
    the provided context, just say, "answer is not available in the context", don't provide a wrong answer.\n\n
    Context:\n{context}\n
    Question: {question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to process user input and generate the response
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load FAISS vector store
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Error loading FAISS index: {e}")
        return
    
    # Perform similarity search
    docs = new_db.similarity_search(user_question)

    # Get the conversational chain and generate response
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])
    print(response)

# Main function for Streamlit app
def main():
    st.set_page_config(page_title="Chat with PDF using Gemini💁", layout="wide")
    st.header("Chat with PDF using Gemini💁")

    # Sidebar to upload PDF files
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("Processing complete. You can now ask questions.")
                    except Exception as e:
                        st.error(f"Error processing PDFs: {e}")
            else:
                st.error("Please upload at least one PDF file.")

    # Main section for user question input
    user_question = "solve the question q1(a) and q1(c) and return their results in an array"
    if st.button("Submit Question") and user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
