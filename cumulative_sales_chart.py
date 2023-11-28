import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px

# Load the dataset
data = pd.read_excel("C:/Users/Chandru/OneDrive/Desktop/Python Visuals/Sample - Superstore.xls", sheet_name="Orders")

# Preprocess the data
data['Order Date'] = pd.to_datetime(data['Order Date'])
data.sort_values('Order Date', inplace=True)
data['Cumulative Sales'] = data['Sales'].cumsum()
data['Year'] = data['Order Date'].dt.year

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in data['Year'].unique()],
                value=data['Year'].unique(),
                multi=True
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cumulative-sales-line-chart')
        ], width=12)
    ])
], fluid=True)

# Define callback to update graph
@app.callback(
    Output('cumulative-sales-line-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_years):
    filtered_data = data[data['Year'].isin(selected_years)]
    fig = px.line(filtered_data, x='Order Date', y='Cumulative Sales', color='Year', title='Cumulative Sales Over Time')
    fig.update_traces(mode='lines+markers+text', textposition='top center')
    fig.update_layout(showlegend=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
