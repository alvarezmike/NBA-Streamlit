import requests
import streamlit as st
import pandas as pd
import base64
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# For more emojis code https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="NBA Stats", page_icon=":basketball:")

# retrieve lottie animation from the web

def load_lottieur(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# animation link from the LottieFiles web page
lottie_coding = load_lottieur("https://assets10.lottiefiles.com/packages/lf20_urtuxtsf.json")

# inserting lottie into web page
st_lottie(lottie_coding, height=200, key="basketball animation")

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit, requests, st_lottie
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('Select Criteria Below')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2022))))

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv',index=False)
#     df = pd.read_csv('output.csv')
#
#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot()

# Barchart
# if st.button('Barchart'):
#     st.header('Age Visualization')
#     st.bar_chart(df_selected_team.Age)





