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
import io
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
    Answer the question as concise and accurate as possible from the provided context, don't provide a wrong answer.\n\n
    Context:\n{context}\n
    Question: {question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
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
    return response["output_text"]

    # Sidebar to upload PDF files
def parse_pdf(pdf_file):
    # Convert bytes object to a file-like object using io.BytesIO
    pdf_file_like = io.BytesIO(pdf_file.read())  # Ensure pdf_file is treated as a file-like object

    # Use PyPDF2 to extract text from PDF
    reader = PdfReader(pdf_file_like)  # Pass the file-like object to PdfReader
    raw_text = ""
    
    # Extract text from all pages
    for page in reader.pages:
        raw_text += page.extract_text()

    # Process the extracted text
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)

def get_numerical_questions():
    # This function interacts with the model to get the correct answer
    # Placeholder for actual implementation
    user_question = "Which are the numerical questions given here.If there two questions with the same question number and both are numerical then add both in the array.Give all the questions in an array only and if there are no questions just return an empty array."
    response = user_input(user_question)
    
    # Assuming the response comes as a string like '[Q.1 (a), Q.1 (c), Q.2 (b), Q.2 (c), Q.3 (b), Q.3 (c), Q.5 (b), Q.5 (c)]'
    
    # Clean the string: Remove brackets and split by comma
    cleaned_response = response.strip('[]')  # Remove the square brackets
    if cleaned_response:  # Check if there is content
        questions_array = [item.strip() for item in cleaned_response.split(',')]  # Split and strip extra spaces
    else:
        questions_array = []  # Return an empty array if no questions are found

    return questions_array


def get_correct_answers(questions_array):
    # This function interacts with the model to get the correct answer
    # For now, it’s a placeholder that always returns '42'
    ques_text = ""
    for q in questions_array:
        ques_text=ques_text+q+','
    print(ques_text)
    user_question = f"Give the answers of the numericals questions in an array of object only, dont give any detailed descriptions."
    response = user_input(user_question)
    cleaned_response = response.strip('[]')  # Remove the square brackets
    if cleaned_response:  # Check if there is content
        answers_array = [item.strip() for item in cleaned_response.split(',')]  # Split and strip extra spaces
    else:
        answers_array = []  # Return an empty array if no questions are found

    return answers_array