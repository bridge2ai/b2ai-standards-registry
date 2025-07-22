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


def calculate_counts(filtered_df):
    """Calculate counts for all dimensions based on filtered data"""
    topic_counts = Counter()
    collection_counts = Counter()
    category_counts = Counter(filtered_df['category'])
    mature_counts = Counter(filtered_df['isMature'])
    ai_counts = Counter(filtered_df['hasAIApplication'])
    open_counts = Counter(filtered_df['isOpen'])

    for idx, row in filtered_df.iterrows():
        for topic in row['topics_list']:
            topic_counts[topic] += 1
        for collection in row['collections_list']:
            collection_counts[collection] += 1

    return topic_counts, collection_counts, category_counts, mature_counts, ai_counts, open_counts


def create_bar_chart(counts_dict, title, chart_id, height=None):
    """Create a horizontal bar chart with proper sizing"""
    if not counts_dict:
        return go.Figure().add_annotation(text="No data", xref="paper", yref="paper", x=0.5, y=0.5)

    items = list(counts_dict.keys())
    values = list(counts_dict.values())

    # Calculate height based on number of items (minimum 400px, 25px per item)
    if height is None:
        height = max(400, len(items) * 25 + 100)

    fig = px.bar(
        x=values,
        y=items,
        orientation='h',
        title=title,
        labels={'x': 'Number of Standards', 'y': ''}
    )

    fig.update_layout(
        height=height,
        yaxis={'categoryorder': 'total ascending'},
        margin={'l': 200, 'r': 20, 't': 50, 'b': 50},
        title_x=0.5
    )

    return fig


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

        # Right column - results and details
        html.Div([
            # Quick filters
            html.Div([
                html.H4("Binary Attributes"),
                html.Div([
                    html.Div([
                        html.Label("Is Mature:"),
                        dcc.Graph(id='mature-chart', style={'height': '200px'})
                    ], style={'width': '32%', 'display': 'inline-block'}),

                    html.Div([
                        html.Label("Has AI Application:"),
                        dcc.Graph(id='ai-chart', style={'height': '200px'})
                    ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),

                    html.Div([
                        html.Label("Is Open:"),
                        dcc.Graph(id='open-chart', style={'height': '200px'})
                    ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'})
                ])
            ], style={'marginBottom': 20}),

            # Results summary
            html.Div([
                html.H4("Filtered Results"),
                html.Div(id='results-summary'),
            ], style={'marginBottom': 20}),

            # Standards table with scrolling
            html.Div([
                html.H4("Standards List"),
                html.Div(
                    id='standards-table',
                    style={
                        'height': '400px',
                        'overflowY': 'scroll',
                        'border': '1px solid #ddd',
                        'padding': '10px'
                    }
                )
            ])

        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})

    ], style={'margin': '20px'}),

    # Store for persistent selections (clicks)
    dcc.Store(id='persistent-filters', data={}),
    # Store for temporary hover filter
    dcc.Store(id='hover-filter', data={})
])


# Separate callback to handle hover clearing
@app.callback(
    Output('hover-filter', 'data'),
    [Input('topic-chart', 'hoverData'),
     Input('category-chart', 'hoverData'),
     Input('collection-chart', 'hoverData'),
     Input('mature-chart', 'hoverData'),
     Input('ai-chart', 'hoverData'),
     Input('open-chart', 'hoverData'),
     Input('clear-filters', 'n_clicks')],
    [State('persistent-filters', 'data')],
    prevent_initial_call=True
)
def update_hover_filter(topic_hover_data, category_hover_data, collection_hover_data,
                        mature_hover_data, ai_hover_data, open_hover_data, clear_clicks, persistent_filters):
    """Update hover filter - clears when no hover data"""

    ctx = callback_context

    # Clear hover filter when clear button is pressed
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'clear-filters.n_clicks':
        return {}

    if persistent_filters is None:
        persistent_filters = {}

    hover_filter = {}

    # Only add to hover filter if not in persistent filters
    if topic_hover_data and 'topic' not in persistent_filters:
        hover_filter['topic'] = topic_hover_data['points'][0]['y']
    if category_hover_data and 'category' not in persistent_filters:
        hover_filter['category'] = category_hover_data['points'][0]['y']
    if collection_hover_data and 'collection' not in persistent_filters:
        hover_filter['collection'] = collection_hover_data['points'][0]['y']
    if mature_hover_data and 'mature' not in persistent_filters:
        hover_filter['mature'] = mature_hover_data['points'][0]['x']
    if ai_hover_data and 'ai' not in persistent_filters:
        hover_filter['ai'] = ai_hover_data['points'][0]['x']
    if open_hover_data and 'open' not in persistent_filters:
        hover_filter['open'] = open_hover_data['points'][0]['x']

    return hover_filter


# Main callback for all interactions
@app.callback(
    [Output('topic-chart', 'figure'),
     Output('category-chart', 'figure'),
     Output('collection-chart', 'figure'),
     Output('mature-chart', 'figure'),
     Output('ai-chart', 'figure'),
     Output('open-chart', 'figure'),
     Output('current-filters', 'children'),
     Output('results-summary', 'children'),
     Output('standards-table', 'children'),
     Output('persistent-filters', 'data')],
    [Input('topic-chart', 'clickData'),
     Input('category-chart', 'clickData'),
     Input('collection-chart', 'clickData'),
     Input('mature-chart', 'clickData'),
     Input('ai-chart', 'clickData'),
     Input('open-chart', 'clickData'),
     Input('clear-filters', 'n_clicks'),
     Input('hover-filter', 'data')],
    [State('persistent-filters', 'data')]
)
def update_dashboard(topic_click, category_click, collection_click, mature_click,
                     ai_click, open_click, clear_clicks, hover_filter, persistent_filters):
    ctx = callback_context

    # Initialize persistent filters if None
    if persistent_filters is None:
        persistent_filters = {}

    if hover_filter is None:
        hover_filter = {}

    # Handle clear button - also clear hover filter
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'clear-filters.n_clicks':
        persistent_filters = {}
        # Note: hover_filter is handled by the separate callback

    # Handle clicks (persistent filters)
    elif ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id']

        if '.clickData' in trigger_id:
            if 'topic-chart' in trigger_id and topic_click:
                persistent_filters['topic'] = topic_click['points'][0]['y']
            elif 'category-chart' in trigger_id and category_click:
                persistent_filters['category'] = category_click['points'][0]['y']
            elif 'collection-chart' in trigger_id and collection_click:
                persistent_filters['collection'] = collection_click['points'][0]['y']
            elif 'mature-chart' in trigger_id and mature_click:
                persistent_filters['mature'] = mature_click['points'][0]['x']
            elif 'ai-chart' in trigger_id and ai_click:
                persistent_filters['ai'] = ai_click['points'][0]['x']
            elif 'open-chart' in trigger_id and open_click:
                persistent_filters['open'] = open_click['points'][0]['x']

    # Combine persistent and hover filters
    all_filters = {**persistent_filters, **hover_filter}

    # Apply filters to dataframe
    filtered_df = df.copy()

    if 'topic' in all_filters:
        mask = filtered_df['topics_list'].apply(lambda x: all_filters['topic'] in x)
        filtered_df = filtered_df[mask]

    if 'category' in all_filters:
        filtered_df = filtered_df[filtered_df['category'] == all_filters['category']]

    if 'collection' in all_filters:
        mask = filtered_df['collections_list'].apply(lambda x: all_filters['collection'] in x)
        filtered_df = filtered_df[mask]

    if 'mature' in all_filters:
        filtered_df = filtered_df[filtered_df['isMature'] == all_filters['mature']]

    if 'ai' in all_filters:
        filtered_df = filtered_df[filtered_df['hasAIApplication'] == all_filters['ai']]

    if 'open' in all_filters:
        filtered_df = filtered_df[filtered_df['isOpen'] == all_filters['open']]

    # Calculate counts based on filtered data
    topic_counts, collection_counts, category_counts, mature_counts, ai_counts, open_counts = calculate_counts(
        filtered_df)

    # Create all charts
    topic_fig = create_bar_chart(dict(topic_counts.most_common()), "Topics by Standard Count", 'topic-chart')
    category_fig = create_bar_chart(dict(category_counts.most_common()), "Categories by Standard Count",
                                    'category-chart')
    collection_fig = create_bar_chart(dict(collection_counts.most_common()), "Collections by Standard Count",
                                      'collection-chart')

    # Binary attribute charts
    mature_fig = px.bar(
        x=list(mature_counts.keys()),
        y=list(mature_counts.values()),
        title="Maturity Status",
        labels={'x': 'Is Mature', 'y': 'Count'}
    ).update_layout(height=200)

    ai_fig = px.bar(
        x=list(ai_counts.keys()),
        y=list(ai_counts.values()),
        title="AI Application",
        labels={'x': 'Has AI Application', 'y': 'Count'}
    ).update_layout(height=200)

    open_fig = px.bar(
        x=list(open_counts.keys()),
        y=list(open_counts.values()),
        title="Open Status",
        labels={'x': 'Is Open', 'y': 'Count'}
    ).update_layout(height=200)

    # Highlight selected bars
    def highlight_selection(fig, filter_key):
        if filter_key in all_filters and fig.data:
            if filter_key in ['topic', 'category', 'collection']:
                # Horizontal bar charts (y-axis values)
                if hasattr(fig.data[0], 'y') and fig.data[0].y:
                    colors = ['red' if str(val) == str(all_filters[filter_key]) else 'blue'
                              for val in fig.data[0].y]
                    fig.data[0].marker.color = colors
            else:
                # Vertical bar charts (x-axis values)
                if hasattr(fig.data[0], 'x') and fig.data[0].x:
                    colors = ['red' if str(val) == str(all_filters[filter_key]) else 'blue'
                              for val in fig.data[0].x]
                    fig.data[0].marker.color = colors
        return fig

    topic_fig = highlight_selection(topic_fig, 'topic')
    category_fig = highlight_selection(category_fig, 'category')
    collection_fig = highlight_selection(collection_fig, 'collection')
    mature_fig = highlight_selection(mature_fig, 'mature')
    ai_fig = highlight_selection(ai_fig, 'ai')
    open_fig = highlight_selection(open_fig, 'open')

    # Create filter display
    filter_parts = []
    for key, value in persistent_filters.items():
        filter_parts.append(f"{key.title()}: {value} (persistent)")
    for key, value in hover_filter.items():
        filter_parts.append(f"{key.title()}: {value} (hover)")

    if filter_parts:
        filter_display = html.Div([
            html.Strong("Active Filters: "),
            html.Br(),
            html.Ul([html.Li(part) for part in filter_parts])
        ])
    else:
        filter_display = "No filters applied - hover to preview, click to persist"

    # Create results
    results_summary = create_results_summary(filtered_df)
    standards_table = create_standards_table(filtered_df)

    return (topic_fig, category_fig, collection_fig, mature_fig, ai_fig, open_fig,
            filter_display, results_summary, standards_table,
            persistent_filters)


def create_results_summary(filtered_df):
    """Create a summary of the filtered results"""
    total = len(filtered_df)

    if total == 0:
        return html.P("No standards match the current filters")

    # Calculate some summary stats
    open_count = len(filtered_df[filtered_df['isOpen'] == 'Yes'])
    ai_count = len(filtered_df[filtered_df['hasAIApplication'] == 'Yes'])
    mature_count = len(filtered_df[filtered_df['isMature'] == 'Yes'])

    return html.Div([
        html.P(f"Total Standards: {total} (of {len(df)})"),
        html.P(f"Open Standards: {open_count} ({open_count / total * 100:.1f}%)"),
        html.P(f"With AI Applications: {ai_count} ({ai_count / total * 100:.1f}%)"),
        html.P(f"Mature Standards: {mature_count} ({mature_count / total * 100:.1f}%)")
    ])


def create_standards_table(filtered_df):
    """Create a scrollable table of standards"""

    if len(filtered_df) == 0:
        return html.P("No standards to display")

    # Create table rows
    table_rows = []
    for idx, row in filtered_df.iterrows():
        topics_str = ', '.join(row['topics_list'][:3])
        if len(row['topics_list']) > 3:
            topics_str += f" (+{len(row['topics_list']) - 3} more)"

        collections_str = ', '.join(row['collections_list'][:2])
        if len(row['collections_list']) > 2:
            collections_str += f" (+{len(row['collections_list']) - 2} more)"

        table_row = html.Tr([
            html.Td(row['acronym'] or row['name'][:30], style={'fontWeight': 'bold'}),
            html.Td(row['category']),
            html.Td(topics_str),
            html.Td(collections_str),
            html.Td(row['isOpen']),
            html.Td(row['hasAIApplication']),
            html.Td(row['isMature'])
        ])
        table_rows.append(table_row)

    # Create the table
    table = html.Table([
        html.Thead([
            html.Tr([
                html.Th("Standard"),
                html.Th("Category"),
                html.Th("Topics"),
                html.Th("Collections"),
                html.Th("Open"),
                html.Th("AI App"),
                html.Th("Mature")
            ])
        ]),
        html.Tbody(table_rows)
    ], style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'border': '1px solid #ddd'
    })

    return table


# Add some CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            table, th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
