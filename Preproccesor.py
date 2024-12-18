import pandas as pd
import numpy as np

def preproceesing(df,region):
    #Filter the data for summer Olympics
    df = df[df['Season'] == 'Summer']
    #Merger the athelets and noc_regions columns
    df = pd.merge(df, region, on='NOC', how='left')
    #drop the duplicates
    df.drop_duplicates(inplace=True)
    #Making the sepearate columns fot gold, silver, and bronze from Medal columns
    #hot encoding the medal column
    x = pd.get_dummies(df['Medal'])
    #Concatinating the hot encoded columns to the df table.
    df = pd.concat([df, x], axis=1)
    return df
