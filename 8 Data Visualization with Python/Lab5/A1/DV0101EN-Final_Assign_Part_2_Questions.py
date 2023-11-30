#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [str(i) for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    # Title
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    
    # Dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    
    dcc.Dropdown(
        id='select-year',
        options=[{'label': year, 'value': year} for year in year_list],
        value='1980',
        placeholder='Select a year',
        style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
    ),
    
    # Output container
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# Callback to enable or disable the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to plot the output graphs for the respective report types
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'),
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Automobile Sales over Recession Period")
        )
        
        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_sales_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales_by_vehicle_type, x='Vehicle_Type', y='Automobile_Sales',
                           title="Average Vehicles Sold by Vehicle Type")
        )
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        expenditure_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(expenditure_by_vehicle_type, values='Advertising_Expenditure', names='Vehicle_Type',
                           title="Total Expenditure Share by Vehicle Type")
        )
        
        # Plot 4: Develop a bar chart for the effect of the unemployment rate on vehicle type and sales
        unemployment_effect = recession_data.groupby(['Year', 'Vehicle_Type'])[['Automobile_Sales', 'unemployment_rate']].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemployment_effect, x='Year', y='Automobile_Sales', color='unemployment_rate',
                           title="Effect of Unemployment Rate on Vehicle Type and Sales")
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]
    
    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == int(selected_year)]
        
        # Plot 1: Yearly Automobile sales using a line chart for the whole period
        yearly_sales = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yearly_sales, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        )
        
        # Plot 2: Total Monthly Automobile sales using a line chart
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )
        
        # Plot 3: Bar chart for the average number of vehicles sold during the given year
        avg_vehicle_data = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avg_vehicle_data, x='Vehicle_Type', y='Automobile_Sales',
                           title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year))
        )
        
        # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
        total_expenditure = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(total_expenditure, values='Advertising_Expenditure', names='Vehicle_Type',
                           title='Total Advertisement Expenditure by Vehicle Type in the year {}'.format(selected_year))
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
