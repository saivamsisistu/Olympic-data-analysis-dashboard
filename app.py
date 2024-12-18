import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import scipy
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import Preproccesor,Helper

df=pd.read_csv("Datasets/athlete_events.csv")
region=pd.read_csv("Datasets/noc_regions.csv")
df=Preproccesor.preproceesing(df,region)
st.sidebar.title("Olympic data analysis")
user_menu=st.sidebar.radio(
    "choose one of the opition",
    ("Medal tally","overall analysis","country wise analysis","Athelete wise analysis")
)

if user_menu=='Medal tally':
    st.sidebar.subheader("Medal Tally")
    #Data frame of Medal tally
    st.header("Medal Tally")


    #selct box code for year and country
    year,country=Helper.Country_Year_List(df)
    selected_year=st.sidebar.selectbox("Select year",year)
    selected_country=st.sidebar.selectbox("Select Country",country)

    #choosen year and country data frame
    medal_tally=Helper.choose(df,selected_year,selected_country)
    if selected_country=="Choose Country" and selected_year=="Choose Year":
        st.header("Overall Medal Tally")
    if selected_country!="Choose Country" and selected_year=="Choose Year":
        st.header("Medal Tally of "+selected_country)
    if selected_country == "Choose Country" and selected_year != "Choose Year":
        st.header("Medal Tally in the year"+str(selected_year) )
    if selected_country != "Choose Country" and selected_year != "Choose Year":
        st.header("Medal Tally of "+selected_country+" in the year "+str(selected_year))
    st.table(medal_tally)

if user_menu=='overall analysis':
    Athlete=df['Name'].unique().shape[0]
    Editions=df['Year'].unique().shape[0]-1
    Events=df['Event'].unique().shape[0]
    Host=df['City'].unique().shape[0]
    Sports=df['Sport'].unique().shape[0]
    Countries=df['region'].unique().shape[0]
    st.header("Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.title("Editions")
        st.title(Editions)
    with col2:
        st.title("Hosts")
        st.title(Host)
    with col3:
        st.title("Countries")
        st.title(Countries)
    with col1:
        st.title('Sports')
        st.title(Sports)
    with col2:
        st.title("Events")
        st.title(Events)
    with col3:
        st.title("Athlete")
        st.title(Athlete)
    st.subheader("Cities and Olympics")
    ex = df[['Year', 'City']]
    new = ex.drop_duplicates(['Year']).set_index('Year')
    st.table(new)

    st.header("Particiaption of nations over time")
    nation_overtime=Helper.Graph_analysis(df,'region')
    fig = px.line(nation_overtime, x='Year', y="region")
    st.plotly_chart(fig)

    st.header("Events of nations over time")
    Events_overtime=Helper.Graph_analysis(df,'Event')
    fig=px.line(Events_overtime,x='Year',y='Event')
    st.plotly_chart(fig)

    st.header("Athelete participation over time")
    Athlete_overtime=Helper.Graph_analysis(df,'Name')
    fig=px.line(Athlete_overtime,x='Year',y='Name')
    st.plotly_chart(fig)

    st.header("Changes in Events over time")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Sport', 'Event', 'Year'])
    pivot = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax=sns.heatmap(pivot,annot=True)
    st.pyplot(fig)

    st.header("Successful Athelete in particular sport ")
    values=df['Sport'].unique().tolist()
    values.sort()
    values.insert(0,'Overall')
    sport=st.selectbox('Choose the sport',values)
    res=Helper.most_successful(df,sport)
    st.table(res)




if user_menu=="country wise analysis":
    st.sidebar.header("Country wise medals Analysis")
    country=df['region'].dropna().unique().tolist()
    country.sort()
    select=st.sidebar.selectbox("Select a Country",country)
    res_df=Helper.Country_medals(df,select)
    fig = px.line(res_df, x='Year', y='Medal')
    st.title(select+" Medall tally over the years")
    st.plotly_chart(fig)

    st.header(select+" Good at follwoing sports")
    try:
        pivot=Helper.Country_wise_sports_performace(df,select)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pivot, annot=True)
        st.pyplot(fig)
    except Exception as e:
        st.text("The available data is in not enough to get the Graph")

    st.header(select+"'s Top 15 players")
    st.table(Helper.Top_playerOfCountry(df,select))

if user_menu=='Athelete wise analysis':
    st.header("Athletes Age distribution ")
    # age,g,s,b=Helper.Age_and_Medal_Distribution(df)
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    age = athelete_df['Age'].dropna()
    g = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    s = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    b = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([age, g, s, b],
                             ['Age distribution', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)

    st.plotly_chart(fig)

    st.header("Age Distribution WRT to Sports(Gold Medalist)")
    x,name=Helper.Age_wrt_gold(df)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.plotly_chart(fig)


    st.header("Athletes height vs strweight distribution")
    values = df['Sport'].unique().tolist()
    values.sort()
    values.insert(0,'Overall')
    sport = st.selectbox('Choose the sport', values)

    res_df=Helper.Weight_vs_Height_wrt_medals(df,sport)
    # Create the scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(x=res_df['Weight'], y=res_df['Height'], hue=res_df['Medal'], style=res_df['Sex'], s=100, ax=ax)
    st.pyplot(fig)








