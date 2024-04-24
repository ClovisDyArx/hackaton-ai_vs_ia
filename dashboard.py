import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.graph_objs as go
import plotly.express as px
from utils import get_new_dataframe


df = get_new_dataframe()

# Initialize the Dash app
ext = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,  title="MINARM", suppress_callback_exceptions=True, external_stylesheets=ext)
server = app.server

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Text Analysis Dashboard'),
    
    # Distribution of Labels
    dcc.Graph(
        id='label-distribution',
        figure=px.pie(df, names='label', title='Label Distribution')
    ),
    
    # Text Length Distribution
    dcc.Graph(
        id='text-length-distribution',
        figure=px.histogram(df, x=df['text'].apply(len), title='Text Length Distribution')
    ),
    
    # src Distribution
    dcc.Graph(
        id='src-distribution',
        figure=px.bar(df['src'].value_counts(), title='src Distribution')
    ),
    
    # Label Distribution by src
    dcc.Graph(
        id='label-by-src',
        figure=px.histogram(df, x='src', color='label', barmode='stack', title='Label Distribution by src')
    ),
    
    # Word Clouds (needs external library such as wordcloud)
    # You need to install the library first: pip install wordcloud
    # Here's a placeholder
    # html.Img(src=wordcloud_image),
    
    # Top N-grams (needs implementation)
    
    # Time Series Analysis (if applicable, needs implementation)
    
    # Correlation Analysis (needs implementation)
])

# Run the Dash app

PORT = 5000
ADDRESS = "0.0.0.0"
if __name__ == '__main__':
    app.run_server(debug=True, port=PORT, host=ADDRESS)


"""
ext = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,  title="Bourse", suppress_callback_exceptions=True, external_stylesheets=ext)
server = app.server

graph_selector = html.Div(children=[
    dcc.Dropdown(
        id='visualization-type',
        options=[
            {'label': 'Lines', 'value': 'lines'},
            {'label': 'Candlesticks', 'value': 'candlesticks'}
        ],
        value='lines'  # valeur par défaut
    )
])

whole_selector = html.Div(children=[
    # Div Milieu
    html.Div(children=[
        html.Label('Select visualization type:'),
        graph_selector,
    ], style={'flex': 1, 'padding': '0 10%'}),

], style={'display': 'flex', 'flexDirection': 'row'})

stock_info_table = dash_table.DataTable(
    id='stock-table',
    columns=[
        {'name': 'Date', 'id': 'date-column'},
        {'name': 'Min', 'id': 'min-column'},
        {'name': 'Max', 'id': 'max-column'},
        {'name': 'Start', 'id': 'start-column'},
        {'name': 'End', 'id': 'end-column'},
        {'name': 'Mean', 'id': 'mean-column'},
        {'name': 'Std Dev', 'id': 'std-dev-column'}
    ],
    page_size=10,
    data=[]
)

# * -={#|#}=- * -={#|#}=- * -={#|#}=- * APP LAYOUT * -={#|#}=- * -={#|#}=- * -={#|#}=- * #
# TODO : compléter le layout.


app.layout = html.Div([
    # Div Haute
    html.Div(children=[  # TODO
        html.Label("Barre des tâches ?"),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    # Div Basse
    html.Div(children=[
        # Div Gauche
        html.Div(children=[
            dcc.Graph(id='stock-graph'),
            whole_selector,

        ], style={'padding': 10, 'flex': 1}),

        # Div Droite
        html.Div(children=[
            html.Label("Infos sur le(s) stock(s) sélectionné(s)"),
            stock_info_table,
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'padding': '5% 0'}),
])


# * -={#|#}=- * -={#|#}=- * -={#|#}=- * CALLBACKS * -={#|#}=- * -={#|#}=- * -={#|#}=- * #
# TODO : ajouter un callback pour chaque action utilisateur.


@callback(
    Output('stock-graph', 'figure'),
    Output('stock-table', 'data'),
    Input('visualization-type', 'value'),
)
def update_graph(selected_stocks, visualization_type, bollinger_switch_value):
    traces = []
    data = []

    for current_stock in selected_stocks:
        if visualization_type == 'lines':
            traces.append(go.Scatter(x=stock_data['Date'],
                                     y=stock_data[current_stock],
                                     mode='lines',
                                     name=current_stock))

    layout = go.Layout(title='Stock Prices', xaxis=dict(title='Date'), yaxis=dict(title='Price'))

    grouped_data = stock_data.groupby(pd.Grouper(key='Date', freq='d'))
    for date, group_data in grouped_data:
        row_data = {
            'date-column': date,
            'min-column': round(group_data[selected_stocks].min().min(), 2),
            'max-column': round(group_data[selected_stocks].max().max(), 2),
            'start-column': round(group_data[selected_stocks].iloc[0, :].min(), 2),
            'end-column': round(group_data[selected_stocks].iloc[-1, :].max(), 2),
            'mean-column': round(group_data[selected_stocks].mean().mean(), 2),
            'std-dev-column': round(group_data[selected_stocks].std().mean(), 2)
        }
        data.append(row_data)

        # Create the figure for the graph
    fig = {'data': traces, 'layout': layout}

    return fig, data


if __name__ == '__main__':
    app.run(debug=True)
"""