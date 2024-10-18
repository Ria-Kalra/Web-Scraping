import streamlit as st
import pandas as pd
import io
import requests
from bs4 import BeautifulSoup

# Page Config
st.set_page_config(page_title="Public Library Scraper", page_icon="📚", layout="centered")

# Custom CSS for dark mode and fonts
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e2f; /* Darker background */
        color: white; /* Default text color */
    }
    .stApp {
        background-color: #1e1e2f; /* Apply to main app container */
    }
    .stTitle, .stHeader, .stSubheader {
        color: white; /* Ensure heading text is white */
        text-align: center; /* Center align text for better visibility */
    }
    .stButton>button {
        background-color: #FF4136; /* Red button */
        color: white; /* Button text color */
        font-size: 18px;
    }
    .css-145kmo2 { /* Selectbox CSS */
        background-color: #333333; /* Dark background for selectbox */
        color: white; /* Text color for selectbox */
    }
    .download-options {
        color: #FFD700; /* Gold color for download options for better visibility */
        font-size: 20px; /* Increase font size */
        font-weight: bold; /* Make font bold */
        margin-top: 20px; /* Add some space above */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Public Library Scraper")

# Function to scrape libraries from a given state
def scrape_libraries(state_url):
    response = requests.get(state_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    libraries = []
    
    # Find library table in the HTML (change based on actual structure)
    for library in soup.select("table tr"):
        cols = library.find_all("td")
        if cols:
            city = cols[0].text.strip()
            name = cols[1].text.strip()
            address = cols[2].text.strip()
            zip_code = cols[3].text.strip()
            phone = cols[4].text.strip() if len(cols) > 4 else "N/A"
            libraries.append({"City": city, "Library": name, "Address": address, "Zip": zip_code, "Phone": phone})
    
    return libraries

# Dropdown for selecting state with all state URLs
states = {
    "Alabama": "https://publiclibraries.com/state/alabama/",
    "Alaska": "https://publiclibraries.com/state/alaska/",
    "Arizona": "https://publiclibraries.com/state/arizona/",
    "Arkansas": "https://publiclibraries.com/state/arkansas/",
    "California": "https://publiclibraries.com/state/california/",
    "Colorado": "https://publiclibraries.com/state/colorado/",
    "Connecticut": "https://publiclibraries.com/state/connecticut/",
    "Delaware": "https://publiclibraries.com/state/delaware/",
    "Florida": "https://publiclibraries.com/state/florida/",
    "Georgia": "https://publiclibraries.com/state/georgia/",
    "Hawaii": "https://publiclibraries.com/state/hawaii/",
    "Idaho": "https://publiclibraries.com/state/idaho/",
    "Illinois": "https://publiclibraries.com/state/illinois/",
    "Indiana": "https://publiclibraries.com/state/indiana/",
    "Iowa": "https://publiclibraries.com/state/iowa/",
    "Kansas": "https://publiclibraries.com/state/kansas/",
    "Kentucky": "https://publiclibraries.com/state/kentucky/",
    "Louisiana": "https://publiclibraries.com/state/louisiana/",
    "Maine": "https://publiclibraries.com/state/maine/",
    "Maryland": "https://publiclibraries.com/state/maryland/",
    "Massachusetts": "https://publiclibraries.com/state/massachusetts/",
    "Michigan": "https://publiclibraries.com/state/michigan/",
    "Minnesota": "https://publiclibraries.com/state/minnesota/",
    "Mississippi": "https://publiclibraries.com/state/mississippi/",
    "Missouri": "https://publiclibraries.com/state/missouri/",
    "Montana": "https://publiclibraries.com/state/montana/",
    "Nebraska": "https://publiclibraries.com/state/nebraska/",
    "Nevada": "https://publiclibraries.com/state/nevada/",
    "New Hampshire": "https://publiclibraries.com/state/new-hampshire/",
    "New Jersey": "https://publiclibraries.com/state/new-jersey/",
    "New Mexico": "https://publiclibraries.com/state/new-mexico/",
    "New York": "https://publiclibraries.com/state/new-york/",
    "North Carolina": "https://publiclibraries.com/state/north-carolina/",
    "North Dakota": "https://publiclibraries.com/state/north-dakota/",
    "Ohio": "https://publiclibraries.com/state/ohio/",
    "Oklahoma": "https://publiclibraries.com/state/oklahoma/",
    "Oregon": "https://publiclibraries.com/state/oregon/",
    "Pennsylvania": "https://publiclibraries.com/state/pennsylvania/",
    "Rhode Island": "https://publiclibraries.com/state/rhode-island/",
    "South Carolina": "https://publiclibraries.com/state/south-carolina/",
    "South Dakota": "https://publiclibraries.com/state/south-dakota/",
    "Tennessee": "https://publiclibraries.com/state/tennessee/",
    "Texas": "https://publiclibraries.com/state/texas/",
    "Utah": "https://publiclibraries.com/state/utah/",
    "Vermont": "https://publiclibraries.com/state/vermont/",
    "Virginia": "https://publiclibraries.com/state/virginia/",
    "Washington": "https://publiclibraries.com/state/washington/",
    "West Virginia": "https://publiclibraries.com/state/west-virginia/",
    "Wisconsin": "https://publiclibraries.com/state/wisconsin/",
    "Wyoming": "https://publiclibraries.com/state/wyoming/"
}

state = st.selectbox("Select a State", list(states.keys()))

# Scrape button
if st.button("Scrape Libraries"):
    state_url = states[state]
    library_data = scrape_libraries(state_url)
    
    # Create DataFrame
    df = pd.DataFrame(library_data)

    # Success message
    st.success(f"Data scraped successfully for {state}!")

    # Display table
    st.dataframe(df)

    # Download Options
    st.markdown("<div class='download-options'>### Download Options:</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f'{state}_libraries.csv',
        mime='text/csv'
    )

    # Download as Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Libraries')
    col2.download_button(
        label="Download as Excel",
        data=excel_buffer.getvalue(),
        file_name=f'{state}_libraries.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Download as JSON
    json = df.to_json(orient="records").encode('utf-8')
    col3.download_button(
        label="Download as JSON",
        data=json,
        file_name=f'{state}_libraries.json',
        mime='application/json'
    )
