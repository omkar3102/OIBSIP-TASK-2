import pandas as pd
import streamlit as st
import datetime as dt
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from IPython.display import HTML


st.title("👨🏻‍🏭 Unemployment Analysis.")
st.write("Made by Omkarnath")

df = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

df.columns = ['State', 'Date', 'Frequency', 'Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate','Region','longitude','latitude']

df['Date'] = pd.to_datetime(df['Date'], dayfirst = True)

#converting the 'frequency' column to category type
df['Frequency'] = df["Frequency"].astype('category')
#extracting the month from date
df['Month'] = df['Date'].dt.month

#create a new column and convert month column values into integer
df['MonthNumber'] = df['Month'].apply(lambda x: int(x))
#create new column and convert monthnumber values into month names
df['MonthName'] = df['MonthNumber'].apply(lambda x: calendar.month_abbr[x])
df['Region'] = df['Region'].astype('category')
#drop the months column we have got month number and month name
df.drop(columns = 'Month', inplace = True)
df.head(3)
st.title(" ")

st.subheader("5-NUMBER_SUMMARY")
st.write(df.describe())
#returns description of the data in the DataFrame. 

#summary of numerical variables which give some information
st.subheader("5- NUMBER SUMMARY OF INFORMATORY VARIABLES")
st.write(round(df[['Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate']].describe().T, 2))

#grouping by 'Region' and finding mean values for the numerical columns
regionStats = df.groupby(['Region'])[['Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']].mean().reset_index()

st.subheader("STATISTICS GROUPED BY REGION")
st.write(round(regionStats, 2))

#constructing heatmap to find the 'pair-wise correlation' values

#dataframe of all  the numerical columns
heatMap = df[['Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate', 'longitude','latitude', 'MonthNumber']]

#constructing on heatmap
heatMap = heatMap.corr()

plt.figure(figsize = (23,8))
sns.heatmap(heatMap, annot = True, cmap = 'twilight_shifted', fmt = '.3f', linewidths = 1)
plt.title("HEATMAP")
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

#EDA- Exploratory Data Analysis
st.header("EXPLORATORY DATA ANALYSIS")
#plot a box-plot to show unemployment rate
fig = px.box(
    df,
    x = 'State',
    y = 'Estimated Unemployment Rate',
    color = 'State',
    title = 'unemploymentRate',
    template = 'plotly'
)
st.subheader("BOX-PLOT [UNEMPLOYMENT RATE IN EACH STATE]")
st.plotly_chart(fig)

#creating a scatter matrix plot to denote relationship
fig = px.scatter_matrix(df,
dimensions = ['Estimated Unemployment Rate', 'Estimated Employed', 'Estimated Labour Participation Rate'],
color = 'Region')
st.subheader("SCATTER MATRIX PLOT")
st.plotly_chart(fig)

#plotting a bar-plot
#finding the average unemployment rate
newDF = df[['Estimated Unemployment Rate', 'State']]

newDF = newDF.groupby('State').mean().reset_index()

#sorting the values in the dataframe
newDF = newDF.sort_values('Estimated Unemployment Rate')

fig = px.bar(newDF,
             x='State',
             y = 'Estimated Unemployment Rate',
             color = 'State',
             title = 'State-wise Average Employment Rate')
st.subheader("BAR-PLOT")
st.plotly_chart(fig)

fig = px.bar(df,
             x = 'Region',
             y = 'Estimated Unemployment Rate',
             animation_frame= 'MonthName',
             color = 'State',
             title = 'Region-wise Unemployment Rate',
             height = 800)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
st.subheader("BAR-PLOT [MONTH-WISE]")
st.plotly_chart(fig)

#creating a new dataframe with state-wise and region wise.
unempDF = df[['State','Region', 'Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']]

unempDF = unempDF.groupby(['Region','State'])['Estimated Unemployment Rate'].mean().reset_index()

#printing the new dataframe
st.subheader("DATAFRAME = STATEWISE & REGIONWISE")

st.write(unempDF.head(4))

#a sunburst chart for unemployment rate
fig = px.sunburst(unempDF,
                  path = ['Region', 'State'],
                  values = 'Estimated Unemployment Rate',
                  title = 'unemployment rate in each region and state',
                  height = 650)

st.subheader("SUNBURST CHART")
st.plotly_chart(fig)

## Impact of Lockdown on States Estimated Employed
st.header("IMPACT OF LOCKDOWN")

#creating a scatter geospatial plot
fig = px.scatter_geo(df,'longitude','latitude',
                     color = "Region",
                     hover_name = "State",
                     size = "Estimated Unemployment Rate",
                     animation_frame = "MonthName",
                     scope = 'asia',
                     title = 'Lockdown Impact throughout India')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1200

#updating the geospatial axes ranges
fig.update_geos(lataxis_range = [5,35],
                lonaxis_range = [65,100],
                oceancolor = "#6dd5ed",
                showocean = True)

st.subheader("SCATTER GEOSPATIAL PLOT")
st.plotly_chart(fig)

#filtering dataset between month 4 and 7 (inclusive)
df47 = df[(df['MonthNumber'] >= 4) & (df['MonthNumber'] <= 7)]

#filtering dataset between month 1 and month 4
df14 = df[(df['MonthNumber'] >= 1) & (df['MonthNumber'] <= 4)]

df47g = df47.groupby('State')['Estimated Unemployment Rate'].mean().reset_index()

df14g = df14.groupby('State')['Estimated Unemployment Rate'].mean().reset_index()

#clubbing the 2 dataframe values
df47g['Unemployment Rate before lockdown'] = df14g['Estimated Unemployment Rate']

#renaming the column values
df47g.columns = ['State','unemploymentRate A/ lockdown', 'unemploymentRate B/ lockdown']

#displaying the top results
st.subheader("DATAFRAME BEFORE & AFTER LOCKDOWN")
st.write(df47g.head())

#computing the percentage change
df47g['% change in unemployment'] = round(df47g['unemploymentRate A/ lockdown'] - df47g['unemploymentRate B/ lockdown'] / df47g['unemploymentRate B/ lockdown'], 2)

df47g = df47g.sort_values('% change in unemployment')

#plotting a 'bar-chart' for the "%change in unemployment A/ lockdown"
fig = px.bar(df47g, x= 'State', y = '% change in unemployment',
             color = '% change in unemployment',
             title = '%  change in Unemployment A/ Lockdown')

st.subheader("BAR-CHART [%CHANGE IN UNEMPLOYMENT]")

st.plotly_chart(fig)

#defining a function to sort values based on impact
def sort_impact(x):
    if x <= 10:
        #impactedState
        return '🥲'
    elif x <= 20:
        #hardImpactedState
        return '🥲🥲'
    elif x <= 30:
        #harderImpactedState
        return '🥲🥲🥲'
    elif x <= 40:
        #hardestImpactedState
        return '🥲🥲🥲🥲'
    return x
#adding a new column to the 'dataframe'
df47g['impactStatus'] = df47g['% change in unemployment'].apply(lambda x:sort_impact(x))

#plotting a "bar-graph" to classify and denote the impact of lockdown on employment for different states
fig = px.bar(df47g,
             y = 'State',
             x = '% change in unemployment',
             color = 'impactStatus',
             title = 'Lockdown Impact on Employment in India')

st.subheader("BAR-GRAPH [CLASSIFYING THE IMPACT FOR DIFFERENT STATES]")

st.plotly_chart(fig)
