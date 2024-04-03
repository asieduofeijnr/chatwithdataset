import os
import streamlit as st
import pandas as pd

from pandasai.responses.response_parser import ResponseParser
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import pyodbc


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

st.title("VISEM")
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
