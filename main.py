import streamlit as st
import pandas as pd
import pyodbc
import os

from pandasai.responses.response_parser import ResponseParser
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from jobspy import scrape_jobs
from PIL import Image


st.set_page_config(page_title="Project Solomon Gets a Job", layout="centered")

image = Image.open('profile.png')


# Use local CSS to manipulate Streamlit default styles
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

portfolio = "https://asieduofeijnr.wixsite.com/solomonresume"
linkedin_url = "https://www.linkedin.com/in/solomonasieduofei/"

# Custom layout with columns
col1, col2 = st.columns([1, 2])

# First column for profile image and quick links
with col1:
    st.image(image, width=200)  # replace with the path to the image
    st.markdown('### Hi, I’m Solomon 👋', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Data Scientist | Project Manager</div>',
                unsafe_allow_html=True)
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


class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.write(result["value"])
        return


st.title("Project 1: 🔍 GEN-AI JOB SEARCH QUERY")
st.markdown("""
    <style>
    .description {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="description">Scrapes jobs from LinkedIn, Glassdoor, Indeed, and ZipRecruiter.</p>',
            unsafe_allow_html=True)

site_name = ["indeed", "linkedin", "zip_recruiter", "glassdoor"]
country_indeed = 'USA'
hours_old = 24

# Using a single column layout for a cleaner look, with spacers for better alignment
st.write("---")  # Adding a horizontal line for visual separation


def get_jobs(site_name, search_term, location, results_wanted, hours_old, country_indeed):
    return scrape_jobs(
        site_name=site_name,
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        country_indeed=country_indeed
    )


col1, col2, col3 = st.columns(3)


with col1:
    search_term = st.text_input(
        "Job Title", "", placeholder="Enter the job title you're searching for")

with col2:
    location = st.text_input(
        "Location", "", placeholder="Enter the job location")

with col3:
    results_wanted = st.number_input("Results Wanted", min_value=1, value=100)

st.write("---")


if st.button("Scrape Jobs", help="Click to start scraping jobs based on your criteria"):
    if search_term:  # Make sure there's a search term provided.
        with st.spinner('Scraping job listings...'):
            st.session_state.jobs = get_jobs(
                site_name, search_term, location, results_wanted, hours_old, country_indeed)
    else:
        # Show an error if search_term is empty.
        st.error("Please enter a job title to search for.")


columns = ['site', 'job_url', 'title', 'description', 'company',
           'location', 'date_posted', 'min_amount', 'max_amount', 'emails']

with st.expander("DataFrame Preview"):
    if 'jobs' in st.session_state and not st.session_state.jobs.empty:
        st.dataframe(st.session_state.jobs[columns])
    else:
        st.info("No data available. Please scrape jobs first.")

st.subheader(f"🔎 Let's Query the Job Search by these columns")
query = st.text_area("🗣️ Chat with Data, Example 'Show me a bar graph grouping jobs by location'",
                     placeholder="Ask something about the job data...")

if query and 'jobs' in st.session_state:
    llm = OpenAI(api_token=os.environ.get('OPENAI_API_KEY'))
    query_engine = SmartDataframe(
        st.session_state.jobs,
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
        },
    )

    answer = query_engine.chat(query)
    st.write(answer)


###################################
SERVER = os.environ.get('VISEMSERVER')
DATABASE = os.environ.get('VISEMSERVERDATABASE')
USERNAME = os.environ.get('VISEMSERVERUSERNAME')
PASSWORD = os.environ.get('VISEMSERVERPASSWORD')

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'
conn = pyodbc.connect(connectionString)
query = """
SELECT VisitorName, VisitorPhoneNumber, VisitorOrganisation, SigninTime, Host, Purpose
FROM dbo.VisitorLog
JOIN dbo.Organisation ON dbo.Organisation.Id = dbo.VisitorLog.CompanyId
Where CompanyId = 2
"""
cursor = conn.cursor()
cursor.execute(query)
data = cursor.fetchall()
data_with_str_dates = [(name, contact, company, pd.Timestamp(visit_time.strftime(
    '%Y-%m-%d %H:%M:%S.%f')), host, visit_type) for name, contact, company, visit_time, host, visit_type in data]
columns = ['Visitor Name', 'Contact', 'Company Visited',
           'Visit Time', 'Host Name', 'Visit Type']


def load_data():
    df = pd.DataFrame(data_with_str_dates, columns=columns)
    return df


if 'df' not in st.session_state:
    st.session_state['df'] = load_data()

#####################################
st.write("----")
st.title("Project 2: VISEM")
st.markdown("""
    <style>
    .description {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="description">Manage Visitors in your workplace.</p>',
            unsafe_allow_html=True)

with st.expander("DataFrame Preview"):
    st.dataframe(st.session_state['df'])

st.subheader(f"🔎 Let's Query the Data")
query = st.text_area("🗣️ Chat with Data, Example 'Show me a bar graph grouping Visits by Days'",
                     placeholder="Ask something about the visitor data...")

if query:
    llm = OpenAI(api_token=os.environ.get('OPENAI_API_KEY'))
    query_engine = SmartDataframe(
        st.session_state['df'],
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
        },
    )

    answer = query_engine.chat(query)
    st.write(answer)
