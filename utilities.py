import os
import pandas as pd
import pyodbc
from jobspy import scrape_jobs


def get_jobs(site_name, search_term, location, results_wanted, hours_old, country_indeed):
    return scrape_jobs(
        site_name=site_name,
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        country_indeed=country_indeed
    )


def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def fetch_visitor_data():
    # Retrieving environment variables for database connection
    SERVER = os.environ.get('VISEMSERVER')
    DATABASE = os.environ.get('VISEMSERVERDATABASE')
    USERNAME = os.environ.get('VISEMSERVERUSERNAME')
    PASSWORD = os.environ.get('VISEMSERVERPASSWORD')

    # Constructing connection string
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'

    # Establishing connection to the database
    conn = pyodbc.connect(connectionString)

    # Defining SQL query to fetch data
    query = """
    SELECT VisitorName, VisitorPhoneNumber, VisitorOrganisation, SigninTime, Host, Purpose
    FROM dbo.VisitorLog
    JOIN dbo.Organisation ON dbo.Organisation.Id = dbo.VisitorLog.CompanyId
    Where CompanyId = 2
    """

    # Executing SQL query and fetching data
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    return data
