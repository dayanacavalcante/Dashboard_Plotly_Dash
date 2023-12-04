# Imports
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# Start the app
app = Dash(__name__)

# Read data
df = pd.read_csv("clean_data.csv")

# Countries with the highest co2 emissions
average_co2_emission_by_country = df.groupby('Entity')['Value_co2_emissions_kt_by_country'].mean()
top_10 = average_co2_emission_by_country.nlargest(10)
filtered_df = df[df['Entity'].isin(top_10.index)]

# Create charts and table
fig = px.bar(filtered_df, x="Year", y="Value_co2_emissions_kt_by_country", color="Entity", barmode="group")
fig_II = px.line(filtered_df, x='Year', y='Electricity from renewables (TWh)', color='Entity')
fig_III = px.line(filtered_df, x='Year', y='Electricity from fossil fuels (TWh)', color='Entity')
fig_IV = px.line(filtered_df, x='Year', y='gdp_per_capita', color='Entity')
fig_V = px.scatter(filtered_df, x='gdp_per_capita', y='Value_co2_emissions_kt_by_country', color='Entity')
fig_VI = go.Figure(data=[go.Table(
    header=dict(values=['Entity', 'Year', 'Value_co2_emissions_kt_by_country', 'Electricity from fossil fuels (TWh)', 'Electricity from renewables (TWh)']),
    cells=dict(values=[filtered_df['Entity'], filtered_df['Year'], filtered_df['Value_co2_emissions_kt_by_country'],
                           filtered_df['Electricity from fossil fuels (TWh)'],filtered_df['Electricity from renewables (TWh)']])
)])

options =list(filtered_df['Entity'].unique())
options.append('All Countries')

# app layout
app.layout = html.Div(
    style={
        'backgroundColor': '#f2f2f2', 
        'padding': '22px' 
    },
    children=[
        html.H1(children='Top 10 CO2 Emitting Countries from the years 2000 to 2019',style={'margin-left': '10px'}),
        html.Span("Trends in CO2 emissions, electricity from fossil fuels and renewable sources, and economic development.", style={'margin-left': '10px','font-size': '18px'}),
        html.H2(children='CO2 emissions in metric tons',style={'margin-left': '10px'}),
    
        dcc.Dropdown(options, value='All Countries', id='country_list', style={'width': '150px', 'margin-bottom': '15px'}),
        
        dcc.Graph(
            id='emissions_co2',
            figure=fig,
        ),
        
        html.H2(children='Electricity generated from renewable sources (hydro, solar, wind, etc.) in terawatt-hours',style={'margin-left': '15px'}),
        dcc.Graph(
            id='use_of_renewable_energy',
            figure=fig_II,
            style={'backgroundColor': '#f2f2f2', 'padding': '20px'}
        ),
        
        html.H2(children='Electricity generated from fossil fuels (coal, oil, gas) in terawatt-hours',style={'margin-left': '15px'}),
        dcc.Graph(
            id='use_of_fossil_fuels_energy',
            figure=fig_III,
            style={'backgroundColor': '#f2f2f2', 'padding': '20px'}
        ),
        
        html.H2(children='Gross domestic product (GDP) per person',style={'margin-left': '15px'}),
        dcc.Graph(
            id='gdp_per_capita',
            figure=fig_IV,
            style={'backgroundColor': '#f2f2f2', 'padding': '20px'}
        ),
        
        html.H2(children='CO2 emissions and GDP per capita',style={'margin-left': '15px'}),
        dcc.Graph(
            id='gdp_per_capita_vs_co2',
            figure=fig_V,
            style={'backgroundColor': '#f2f2f2', 'padding': '20px'}
        ), 
        
        dcc.Graph(
            id='table',
            figure=fig_VI,
            style={'backgroundColor': '#f2f2f2', 'padding': '20px'})
            ]
    )

@app.callback(
    Output('emissions_co2', 'figure'),
    Input('country_list', 'value')
)
def update_output(value):
    if value == "All Countries":
        fig = px.bar(filtered_df, x="Year", y="Value_co2_emissions_kt_by_country", color="Entity", barmode="group")
        fig.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = df.loc[df['Entity']==value, :]
        fig = px.line(filtered_table, x='Year', y='Value_co2_emissions_kt_by_country', color='Entity')
        fig.update_layout(paper_bgcolor='#f2f2f2')
    return fig

@app.callback(
    Output('use_of_renewable_energy', 'figure'),
    Input('country_list', 'value')
)

def update_output_II(value):
    if value == "All Countries":
        fig_II = px.bar(filtered_df, x="Year", y="Electricity from renewables (TWh)", color="Entity", barmode="group")
        fig_II.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = df.loc[df['Entity']==value, :]
        fig_II = px.line(filtered_table, x='Year', y='Electricity from renewables (TWh)', color='Entity')
        fig_II.update_layout(paper_bgcolor='#f2f2f2')
    return fig_II

@app.callback(
    Output('use_of_fossil_fuels_energy', 'figure'),
    Input('country_list', 'value')
)
def update_output_III(value):
    if value == "All Countries":
        fig_III = px.bar(filtered_df, x="Year", y="Electricity from fossil fuels (TWh)", color="Entity", barmode="group")
        fig_III.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = df.loc[df['Entity']==value, :]
        fig_III = px.line(filtered_table, x='Year', y='Electricity from fossil fuels (TWh)', color='Entity' )
        fig_III.update_layout(paper_bgcolor='#f2f2f2', )
    return fig_III

@app.callback(
    Output('gdp_per_capita', 'figure'),
    Input('country_list', 'value')
)
def update_output_IV(value):
    if value == "All Countries":
        fig_IV = px.bar(filtered_df, x="Year", y="gdp_per_capita", color="Entity", barmode="group")
        fig_IV.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = filtered_df.loc[df['Entity']==value, :]
        fig_IV = px.line(filtered_table, x='Year', y='gdp_per_capita', color='Entity') 
        fig_IV.update_layout(paper_bgcolor='#f2f2f2')
    return fig_IV

@app.callback(
    Output('gdp_per_capita_vs_co2', 'figure'), 
    Input('country_list', 'value')
)
def update_output_V(value):
    if value == "All Countries":
        fig_V = px.scatter(filtered_df, x='gdp_per_capita', y='Value_co2_emissions_kt_by_country', color='Entity')
        fig_V.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = filtered_df.loc[df['Entity']==value, :]
        fig_V = px.scatter(filtered_table, x='gdp_per_capita', y='Value_co2_emissions_kt_by_country', color='Entity')
        fig_V.update_layout(paper_bgcolor='#f2f2f2')
    return fig_V

@app.callback(
    Output('table', 'figure'), 
    Input('country_list', 'value')
)
def update_output_V(value):
    if value == "All Countries":
        fig_VI = go.Figure(data=[go.Table(
        header=dict(values=['Entity', 'Year', 'Value_co2_emissions_kt_by_country', 'Electricity from fossil fuels (TWh)', 'Electricity from renewables (TWh)']),
        cells=dict(values=[filtered_df['Entity'], filtered_df['Year'], filtered_df['Value_co2_emissions_kt_by_country'],
                           filtered_df['Electricity from fossil fuels (TWh)'],filtered_df['Electricity from renewables (TWh)']])
        )])
        fig_VI.update_layout(paper_bgcolor='#f2f2f2')
    else:
        filtered_table = filtered_df.loc[df['Entity']==value, :]
        fig_VI = go.Figure(data=[go.Table(
        header=dict(values=['Entity', 'Year', 'Value_co2_emissions_kt_by_country', 'Electricity from fossil fuels (TWh)', 'Electricity from renewables (TWh)']),
        cells=dict(values=[filtered_table['Entity'], filtered_table['Year'], filtered_table['Value_co2_emissions_kt_by_country'],
                           filtered_table['Electricity from fossil fuels (TWh)'],filtered_table['Electricity from renewables (TWh)']])
)])
        fig_VI.update_layout(paper_bgcolor='#f2f2f2')
    return fig_VI

if __name__ == '__main__':
    app.run(debug=True)
