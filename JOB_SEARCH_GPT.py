import os
import streamlit as st

from pandasai.responses.response_parser import ResponseParser
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from jobspy import scrape_jobs


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


st.title("🔍 Project Solomon Gets a Job")
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

if search_term:
    def get_jobs(site_name, search_term, location, results_wanted, hours_old, country_indeed):
        return scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed
        )


if st.button("Scrape Jobs", help="Click to start scraping jobs based on your criteria") or not 'jobs' in st.session_state:
    with st.spinner('Scraping job listings...'):
        st.session_state.jobs = get_jobs(
            site_name, search_term, location, results_wanted, hours_old, country_indeed)


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
