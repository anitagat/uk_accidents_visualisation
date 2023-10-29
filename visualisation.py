import plotly.express as px
import pandas as pd
from pandas import DataFrame

# # Plot accident counts per year
# fig = px.line(df, x='Year', y='Accident_Number', title='Accidents per Year')
# fig.show()

df_2017 = pd.read_csv("accidentsheatmap.csv")

# Heatmap 
fig = px.scatter_geo(df_2017,
                     lat='latitude',
                     lon='longitude',
                     color='district',
                     title='Density of Accidents in Different Districts for 2017',
                     opacity=0.5,  # Adjust as needed
                     template='plotly',
                     projection='natural earth',
                     scope='europe')
fig.update_geos(showcoastlines=True, coastlinecolor="blue", showland=True, landcolor="lightgreen")
fig.show()

fig.write_html("accidents_year.html")