import pandas as pd
import numpy as np
def Medal_Tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Event', 'Sport', 'Medal', 'region'])
    medals = medal_tally.groupby('region')[["Gold", "Silver", "Bronze"]].sum().sort_values('Gold', ascending=False).reset_index()
    medals['tatal']=medals['Gold']+medals['Silver']+medals['Bronze']
    return medals
def Country_Year_List(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Choose Year')
    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0,'Choose Country')
    return years,Country
def choose(df,year,country):
      medal_tally=df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Event', 'Sport', 'Medal', 'region'])
      flag=0
      if year=="Choose Year" and country=="Choose Country":
        temp_df=medal_tally
      if year!="Choose Year" and country=="Choose Country":
        temp_df=medal_tally[medal_tally['Year']==year]
      if year=="Choose Year" and country!="Choose Country":
        flag=1
        temp_df=medal_tally[medal_tally['region']==country]
      if year!="Choose Year" and country!="Choose Country":
        temp_df=medal_tally[(medal_tally['Year']==year) & (medal_tally['region']==country)]
      if flag==1:
        data=temp_df.groupby('Year')[["Gold", "Silver", "Bronze"]].sum().sort_values('Year')
        data['total']=data['Gold']+data['Silver']+data['Bronze']
        return data
      else:
        data=temp_df.groupby('region')[["Gold", "Silver", "Bronze"]].sum().sort_values('Gold', ascending=False).reset_index()
        data['total']=data['Gold']+data['Silver']+data['Bronze']
        return data
def Graph_analysis(df,col):
    nation_overtime = df[['Year', col]].drop_duplicates(['Year',col])[
        'Year'].value_counts().reset_index().sort_values('Year')
    nation_overtime.rename(columns={'count':col}, inplace=True)
    return nation_overtime


def most_successful(df, sport):
    temp = df.dropna(subset='Medal')
    if (sport != 'Overall'):
        temp = temp[temp['Sport'] == sport]

    res = temp[['Name']].value_counts().reset_index().merge(df, on='Name', how='left')
    x = res[['Name', 'region', 'Sport', 'count']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals count'}, inplace=True)
    return x

def Country_medals(df,country):
    tem_df= df.dropna(subset='Medal')
    tem_df.drop_duplicates(subset=["Team", 'NOC', 'Games', "Year", 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == country]
    new_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return new_df

def Country_wise_sports_performace(df,country):
    tem_df = df.dropna(subset='Medal')
    tem_df.drop_duplicates(subset=["Team", 'NOC', 'Games', "Year", 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == country]
    pivot = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return pivot
def Top_playerOfCountry(df, country):
    temp = df.dropna(subset='Medal')
    temp = temp[temp['region'] == country]

    res = temp[['Name']].value_counts().reset_index().merge(df, on='Name', how='left')
    x = res[['Name', 'Sport', 'count']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals count'}, inplace=True)
    return x.head(15)

def Age_wrt_gold(df):
    famous_sports = [
        'Alpinism',
        'Archery',
        'Art Competitions',
        'Athletics',
        'Badminton',
        'Baseball',
        'Basketball',
        'Basque Pelota',
        'Beach Volleyball',
        'Boxing',
        'Canoeing',
        'Cricket',
        'Croquet',
        'Cycling',
        'Diving',
        'Equestrianism',
        'Fencing',
        'Figure Skating',
        'Football',
        'Golf',
        'Gymnastics',
        'Handball',
        'Hockey',
        'Ice Hockey',
        'Judo',
        'Lacrosse',
        'Modern Pentathlon',
        'Motorboating',
        'Polo',
        'Racquets',
        'Rhythmic Gymnastics',
        'Rowing',
        'Rugby',
        'Rugby Sevens',
        'Sailing',
        'Shooting',
        'Softball',
        'Swimming',
        'Synchronized Swimming',
        'Table Tennis',
        'Taekwondo',
        'Tennis',
        'Trampolining',
        'Triathlon',
        'Tug-Of-War',
        'Volleyball',
        'Water Polo',
        'Weightlifting',
        'Wrestling'
    ]

    x = []
    name = []
    for sport in famous_sports:
        temp_df = df[df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        # Check if age_data has enough elements for KDE calculation and sufficient variation
        if len(age_data) > 1 and np.var(age_data) > 0:
            x.append(age_data)
            name.append(sport)
    return x,name

def Weight_vs_Height_wrt_medals(df,sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    athelete_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        res = athelete_df[athelete_df['Sport'] == sport]
        return res
    else:
        return athelete_df


