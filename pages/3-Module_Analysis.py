import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import altair as alt 
import plotly.express as px
from navigation import make_sidebar
from millify import millify # shortens values (10_000 ---> 10k)
from streamlit_extras.metric_cards import style_metric_cards # beautify metric card with css

make_sidebar()


# Import the dataset
image = "CGHPI.png"
df = pd.read_csv('Datasets/Final_dataset.csv', encoding='ISO-8859-1')
df1 = pd.read_csv('Datasets/Gender.csv', encoding='ISO-8859-1')
df2 = pd.read_csv('Datasets/Ageband.csv', encoding='ISO-8859-1')

password = st.session_state['password']

# Streamlit application
def app():
    # Main page content
    #st.set_page_config(page_title = 'AIC Dashboard -- Section Analysis', page_icon='🇺🇬',layout='wide')

    title = f'Module Analysis -- {password}'
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
            <h2 style='text-align: center'>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.title('Enter your selections here!')

    # Ensure the Score column is sorted
    #program_selected = st.sidebar.selectbox('Select Institution', df['Program'].unique())
    module_selected = st.sidebar.selectbox('Select Module', df['Module_name'].unique())
    #question_selected = st.sidebar.selectbox('Select Question', df[df['Module_name'] == module_selected]['Question'].unique())
    #st.sidebar.markdown(f"#### You selected: {question_selected}")
    
    # Update last viewed module and part
    st.session_state.last_module = module_selected
    #st.session_state.last_question = question_selected
    
    plot_selected = st.sidebar.selectbox('Select Visualization Type',['Bar Plot','Heat Map','Table'],index=0)

    # creates the container for metric card
    dash_1 = st.container()

    with dash_1:
        # Get Description data
        total_ppl = df1[df1.Program==password].Q4.sum()
        record_f = df1[(df1.Program==password)&(df1.Gender=='Female')]
        total_f = record_f['Q4'].iloc[0] if not record_f.empty else 0
        record_m = df1[(df1.Program==password)&(df1.Gender=='Male')]
        total_m = record_m['Q4'].iloc[0] if not record_m.empty else 0

        col1, col2, col3 = st.columns(3)
        # create column span
        col1.metric(label="Total Respondents", value= millify(total_ppl, precision=2))

        col2.metric(label="Female Respondents", value= millify(total_f, precision=2))

        col3.metric(label="Male Respondents", value= millify(total_m, precision=2))

        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227")

    # creates the container for metric card
    dash_2 = st.container()

    with dash_2:
        # Get Description data
        record_18_35 = df2[(df2.Program==password)&(df2.AgeBand=='18-35 years')]
        total_18_35 = record_18_35['Q3'].iloc[0] if not record_18_35.empty else 0
        record_36_45 = df2[(df2.Program==password)&(df2.AgeBand=='36-45 years')]
        total_36_45 = record_36_45['Q3'].iloc[0] if not record_36_45.empty else 0
        record_46_55 = df2[(df2.Program==password)&(df2.AgeBand=='46-55 years')]
        total_46_55 = record_46_55['Q3'].iloc[0] if not record_46_55.empty else 0
        record_56 = df2[(df2.Program==password)&(df2.AgeBand=='56 years and above')]
        total_56 = record_56['Q3'].iloc[0] if not record_56.empty else 0

        col1, col2, col3, col4 = st.columns(4)
        # create column span
        col1.metric(label="18-35", value= millify(total_18_35, precision=2))

        col2.metric(label="36-45", value= millify(total_36_45, precision=2))

        col3.metric(label="46-55", value= millify(total_46_55, precision=2))
        
        col4.metric(label="56+", value= millify(total_56, precision=2))
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227")

        
    # Filter data based on selections
    filtered_data = df[(df['Module_name'] == module_selected) & 
                        (df['Program'] == password)]
    
    # creates the container for metric card
    dash_3 = st.container()

    with dash_3:
        # Get Desc
        if not filtered_data.empty:
            if plot_selected == 'Bar Plot':
                st.write("")
                
                # Define the desired order for the Response categories
                response_order = ['Strongly Agree', 'Agree', 'Somewhat Agree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree']

                # Ensure the 'Response' column is treated as a categorical variable with the specified order
                filtered_data['Response'] = pd.Categorical(filtered_data['Response'], categories=response_order, ordered=True)

                # Assign an ordinal value to each response type for sorting
                filtered_data['response_order'] = filtered_data['Response'].cat.codes

                # Now create the Altair chart
                chart = alt.Chart(filtered_data).mark_bar().encode(
                    y=alt.Y('Qn:N', title='Question'),
                    x=alt.X('sum(Count):Q', title='Count'),
                    color=alt.Color('Response:N', 
                                    legend=alt.Legend(title="Response"),
                                    sort=response_order
                                ),
                    order=alt.Order(
                        'response_order:O',  # Use the calculated ordinal value to enforce the stacking order
                        sort='ascending'
                    ),
                    tooltip=['Qn','Question','Response', 'sum(Count)']
                ).properties(
                    title=f'{password} -- Bar Plot of Distribution of Responses Across Questions within {module_selected}',
                    width=1000,
                    height=600
                ).interactive()

                st.altair_chart(chart, use_container_width=True)


            elif plot_selected == 'Heat Map':
                st.write("")
                
                # Creating a heatmap
                heatmap = alt.Chart(filtered_data).mark_rect().encode(
                    x=alt.X('Qn:N', axis=alt.Axis(labelAngle=+0), title='Question'),
                    y=alt.Y('Response:N', title='Response', sort=['Strongly Agree', 'Agree', 'Somewhat Agree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree']),
                    color=alt.Color('Count:Q', scale=alt.Scale(scheme='viridis'), title='Count'),
                    tooltip=['Qn','Question', 'Response', 'Count']
                ).properties(
                    title=f'{password} -- Heatmap of Distribution of Response Across Questions within {module_selected}',
                    width=1000,
                    height=600
                ).interactive()

                st.altair_chart(heatmap, use_container_width=True)
                
                
                
            
            else:
                response_order = ['Strongly Agree', 'Agree', 'Somewhat Agree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree']
                filtered_data['order'] = filtered_data['Response'].apply(lambda x: response_order.index(x))
                records = filtered_data.sort_values(by=['Qn','order'])[['Program', 'Module_name','Qn','Question','Response','Count']].reset_index().drop(columns='index')
                st.markdown(f"#### {password} -- Distrbution of Response Across Questions within {module_selected} are shown below:")
                st.dataframe(records)

        else:
            st.markdown("### No data available for the selected criteria.")

if __name__ == "__main__":
    app()