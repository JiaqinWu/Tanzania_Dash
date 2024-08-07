import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import altair as alt 
import numpy as np
from navigation import make_sidebar

make_sidebar()

# Import the dataset
image = "CGHPI.png"

password = st.session_state['password']

# Streamlit application
def app():
    # Main page content
    #st.set_page_config(page_title = 'UCMB Dashboard -- Uganda SCORE Survey', page_icon='🇺🇬',layout='wide')

    #st.image(image, width=200, use_column_width=False)
    #st.title('Sustainable Capacity of Local Organizations to Reach and End the HIV/AIDS Pandemic (SCORE)')

    title = f'Tanzania Organizational Effectiveness Survey - {password}'
    col1, col2, col3 = st.columns([4, 1, 5])

    with col1:
        st.write("")

    with col2:
        st.image(image, width=250)

    with col3:
        st.write("")

    # Center the image and title using HTML and CSS in Markdown
    st.markdown(
        f"""
        <style>
        .centered {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 30vh;
            text-align: center;
        }}
        </style>
        <div class="centered">
            <h1 style='text-align: center'>{title}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    st.markdown("""
    ### ACKNOWLEDGEMENT

    """)

    st.markdown("""
    ### INTRODUCTION

    """)
                            
    st.markdown("""
    ### USAGE

    Feel free to explore any tab to interact with the data!
    """)





if __name__ == "__main__":
    app()
