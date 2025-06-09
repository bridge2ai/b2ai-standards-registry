import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, callback_context
import json
import networkx as nx
from collections import defaultdict, Counter
import ast


# Load and prepare the data
def load_and_prepare_data():
    # Load the DST_denormalized data
    df = pd.read_csv('DST_denormalized.csv')

    # Parse JSON fields
    def safe_json_parse(x):
        if pd.isna(x) or x == '':
            return []
        try:
            return json.loads(x)
        except:
            return []

    df['topics_list'] = df['topic'].apply(safe_json_parse)
    df['collections_list'] = df['collections'].apply(safe_json_parse)

    return df

# Initialize the Dash app
app = dash.Dash(__name__)

# Load data
df = load_and_prepare_data()

# App layout
app.layout = html.Div([
    html.H1("Interactive Standards Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),

    # Control panel
    html.Div([
        html.H3("Filters & Selections"),
        html.P("Hover to preview filter, Click to apply persistent filter. Multiple persistent filters combine."),
        html.Button("Clear All Filters", id="clear-filters", n_clicks=0),
        html.Div(id="current-filters", style={'marginTop': 10})
    ], style={'margin': '20px', 'padding': '10px', 'border': '1px solid #ddd'}),

    # Main content area
    html.Div([
        # Left column - dimension lists
        html.Div([
            # Topics
            html.Div([
                html.H4("Topics"),
                dcc.Graph(id='topic-chart', style={'height': 'auto'})
            ], style={'marginBottom': 20}),

            # Categories
            html.Div([
                html.H4("Categories"),
                dcc.Graph(id='category-chart', style={'height': 'auto'})
            ], style={'marginBottom': 20}),

            # Collections
            html.Div([
                html.H4("Collections"),
                dcc.Graph(id='collection-chart', style={'height': 'auto'})
            ])

        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ])
])


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
