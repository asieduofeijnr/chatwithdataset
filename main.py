import os
import pandas as pd

import streamlit as st
from PIL import Image

# Importing classes and utilities
from classes import *
from utilities import *

# Importing llama index related modules
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext

# Importing pandasai related modules
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# Setting API Key
API_KEY = os.getenv('OPENAI_API_KEY')

# Setting Streamlit page configuration
st.set_page_config(page_title="Solomons Portfolio", layout="centered")

# Loading profile image
image = Image.open('profile.png')

# Customizing Streamlit default styles
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: 550;
    }
    .info-text {
        font-size:20px !important;
    }
    .python-code {
        background: #333;
        color: #eee;
        padding: 10px;
        border-radius: 10px;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Defining portfolio and LinkedIn URLs
portfolio = "https://asieduofeijnr.wixsite.com/solomonresume"
linkedin_url = "https://www.linkedin.com/in/solomonasieduofei/"

# Custom layout with columns
col1, col2 = st.columns([1, 2])

# First column for profile image and quick links
with col1:
    st.image(image, width=200)  # Displaying profile image
    st.markdown('### Hi, I’m Solomon 👋', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Data Scientist | Project Manager</div>',
                unsafe_allow_html=True)
    # Adding portfolio and LinkedIn buttons
    st.markdown(
        f"<a href='{portfolio}' target='_blank'><button style='width:100%'>Portfolio</button></a>", unsafe_allow_html=True)
    st.markdown(
        f"<a href='{linkedin_url}' target='_blank'><button style='width:100%'>LinkedIn</button></a>", unsafe_allow_html=True)

# Second column for python code display
with col2:
    st.markdown("""
    ```python
    class AboutSolomon:
        def __init__(self):
            self.occupation = 'Data Scientist | Project Manager'
            self.skills = (
                'Python',
                'Machine Learning',
                'A/B testing',
                'Generative AI',
                'Project Management'
            )
            self.hobbies = (
                '🏋️‍♂️ Powerlifting',
                '🌶 Eating spicy food',
                '👑 Playing chess'
            )
            self.current_favorite_music_artists = (
                'The Weekend',
                'Coldplay',
                'Imagine Dragons'
            )
            self.fun_fact = 'I built an autonomous Robot!'
    ```
    """, unsafe_allow_html=True)

    # Add more Streamlit components or custom HTML/CSS as needed for your content


st.title("Project 1: 🔍 GEN-AI JOB SEARCH QUERY")

# Customizing Markdown styles
st.markdown("""
    <style>
    .description {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Providing description of the project
st.markdown('<p class="description">Scrapes jobs from LinkedIn, Glassdoor, Indeed, and ZipRecruiter.</p>',
            unsafe_allow_html=True)

site_name = ["indeed", "linkedin", "zip_recruiter", "glassdoor"]
country_indeed = 'USA'
hours_old = 24

# Adding a horizontal line for visual separation
st.write("---")

# Using a single column layout for a cleaner look, with spacers for better alignment
col1, col2, col3 = st.columns(3)

# Text input for job title
with col1:
    search_term = st.text_input(
        "Job Title", "", placeholder="Enter the job title you're searching for")

# Text input for job location
with col2:
    location = st.text_input(
        "Location", "", placeholder="Enter the job location")

# Number input for number of results wanted
with col3:
    results_wanted = st.number_input("Results Wanted", min_value=1, value=100)

# Adding another horizontal line for visual separation
st.write("---")

# Button to initiate job scraping
if st.button("Scrape Jobs", help="Click to start scraping jobs based on your criteria"):
    if search_term:  # Make sure there's a search term provided.
        with st.spinner('Scraping job listings...'):
            st.session_state.jobs = get_jobs(
                site_name, search_term, location, results_wanted, hours_old, country_indeed)
    else:
        # Show an error if search_term is empty.
        st.error("Please enter a job title to search for.")

# Defining columns for job dataframe preview
columns = ['site', 'job_url', 'title', 'description', 'company',
           'location', 'date_posted', 'min_amount', 'max_amount', 'emails']

# Expander for DataFrame Preview
with st.expander("DataFrame Preview"):
    if 'jobs' in st.session_state and not st.session_state.jobs.empty:
        st.dataframe(st.session_state.jobs[columns])
    else:
        st.info("No data available. Please scrape jobs first.")

# Section for querying the job search by specific columns
st.subheader(f"🔎 Let's Query the Job Search by these columns")

# Text area for user to input query
query = st.text_area("🗣️ Chat with Data, Example 'Show me a bar graph grouping jobs by location'",
                     placeholder="Ask something about the job data...")

# Processing user query if provided and jobs data is available
if query and 'jobs' in st.session_state:
    llm = OpenAI(api_token=API_KEY)
    query_engine = SmartDataframe(
        st.session_state.jobs,
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
        },
    )

    answer = query_engine.chat(query)
    st.write(answer)


# PROJECT 2
data = fetch_visitor_data()

# Converting fetched data to DataFrame with string dates converted to Timestamp
data_with_str_dates = [(name, contact, company, pd.Timestamp(visit_time.strftime(
    '%Y-%m-%d %H:%M:%S.%f')), host, visit_type) for name, contact, company, visit_time, host, visit_type in data]
columns = ['Visitor Name', 'Contact', 'Company Visited',
           'Visit Time', 'Host Name', 'Visit Type']

# Storing DataFrame in session state if not already present
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame(data_with_str_dates, columns=columns)

# Adding horizontal line for visual separation
st.write("----")

# Displaying title for Project 2
st.title("Project 2: VISEM")

# Customizing Markdown styles
st.markdown("""
    <style>
    .description {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Providing description for Project 2
st.markdown('<p class="description">Manage Visitors in your workplace.</p>',
            unsafe_allow_html=True)

# Expander for DataFrame Preview
with st.expander("DataFrame Preview"):
    st.dataframe(st.session_state['df'])

# Subheader for querying the data
st.subheader(f"🔎 Let's Query the Data")

# Text area for user to input query
query = st.text_area("🗣️ Chat with Data, Example 'Show me a bar graph grouping Visits by Days'",
                     placeholder="Ask something about the visitor data...")

# Processing user query if provided
if query:
    llm = OpenAI(api_token=API_KEY)
    query_engine = SmartDataframe(
        st.session_state['df'],
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
        },
    )

    answer = query_engine.chat(query)
    st.write(answer)

# PROJECT 3
# Adding horizontal line for visual separation
st.write("----")

# Displaying title for Project 3
st.title("Project 3: Custom LLM Model with llama.index")

documents = []
uploaded_files = st.file_uploader("Upload files (text or PDF)", type=[
                                  'txt', 'pdf'], accept_multiple_files=True)

if uploaded_files is not None:
    # Creating a folder named "data" to store the uploaded files
    create_folder_if_not_exists("test_data")

    # Iterating through uploaded files and saving them
    for file_num, file in enumerate(uploaded_files):
        # Saving each uploaded file in the "data" folder with its original name
        with open(os.path.join("test_data", file.name), "wb") as f:
            f.write(file.getbuffer())
        st.success(
            f"File '{file.name}' uploaded successfully and stored in the 'data' folder.")

try:
    # Trying to load files assuming this is where you're trying to load them
    documents = SimpleDirectoryReader(
        'test_data').load_data(show_progress=True)
except ValueError as e:
    # Displaying error message if loading fails
    st.error(str(e))

# Configuring service context
embed_model_bge = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Configuring service context with default settings
service_context = ServiceContext.from_defaults(embed_model=embed_model_bge,
                                               chunk_size=1000,
                                               chunk_overlap=20)

# Creating index from documents
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context)

# Creating query engine
query_engine = index.as_query_engine()

# Subheader for querying the uploaded files
st.subheader(f"🔎 Let's Query the File(s)")

# Text area for user to input query
query = st.text_area("🗣️ Chat with Data",
                     placeholder="Ask something about the document uploaded")

# Processing user query if provided
if query:
    response = query_engine.query(query)
    st.markdown(response)
