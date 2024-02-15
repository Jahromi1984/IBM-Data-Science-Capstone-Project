# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:38:19 2024

@author: KAZ76504
"""

### Hands-on Lab: Build an Interactive Dashboard with Ploty Dash

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import webbrowser
from threading import Timer

port = 8050 # or simply open on the default `8050` port

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

#folder = '//Users//alikazemijahromi//Library//CloudStorage//OneDrive-Personal//Machine Learning//Coursera//IMB Data Science Specialization//Course 10//Week 3//'
folder = 'C:\\Users\\KAZ76504\\OneDrive - Personal\\OneDrive\\Machine Learning\\Coursera\\IMB Data Science Specialization\\Course 10\\Week 3\\'
filename = 'spacex_launch_dash.csv'
path = folder + filename
spacex_df = pd.read_csv(path)

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] + [
                                        {'label':l, 'value':l}
                                        for l in spacex_df['Launch Site'].unique().tolist()
                                    ],
                                    value="ALL",
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df
        fig = px.pie(data, values='class', names='Launch Site',
                title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data = (spacex_df
            .loc[spacex_df['Launch Site'] == entered_site]
            .groupby('class')[['class']]
            .count()
            .rename({"class":"class_count"}, axis=1)
            .reset_index()
        )
        fig = px.pie(data, values='class_count', names='class',
                title=f'Total Success Launches for site "{entered_site}"')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [
                  Input(component_id='site-dropdown', component_property='value'),
                  Input(component_id='payload-slider', component_property='value')
              ])
def get_scatter_plot(entered_site, entered_payload):
    min_value = entered_payload[0]
    max_value = entered_payload[1]
    data = spacex_df.loc[
        (spacex_df['Payload Mass (kg)'] >= min_value) &
        (spacex_df['Payload Mass (kg)'] <= max_value)
    ]
    if entered_site == 'ALL':
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                title=f'Correlation between Payload and Success for all Sites')
        return fig
    else:
        data = data.loc[data['Launch Site'] == entered_site]
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                title=f'Correlation between Payload and Success for site "{entered_site}"')
        return fig

# Run the application                   
if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, port=port)













































