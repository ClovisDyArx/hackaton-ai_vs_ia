import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.graph_objs as go
import plotly.express as px
from utils import get_new_dataframe, get_dataframe
from wordcloud import WordCloud
import base64
import io

# Initialize the Dash app
ext = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,  title="MINARM", suppress_callback_exceptions=True, external_stylesheets=ext)
server = app.server

#### NEW DATAFRAME ####

df = get_new_dataframe()

tmp_df = pd.DataFrame()
tmp_df['label'] = df['label'].copy()
tmp_df["label"] = tmp_df["label"].apply(lambda x: "humain" if x == 1 else "IA")
pie_graph = html.Div(children=[
    dcc.Graph(
        id='label-distribution',
        figure=px.pie(tmp_df, names='label', labels={1: 'humains', 0: 'IAs'}, title='Distribution des Labels (humains vs ia)')
    ),
])

histogram_figure = px.histogram(df, x=df['text'].apply(len), title='Distribution de la longueur des textes')
histogram_figure.update_xaxes(range=[0, 7000])
text_len_graph = html.Div(children=[
    dcc.Graph(
        id='text-length-distribution',
        figure=histogram_figure
    ),
])

n = 20
top_sources = df['src'].value_counts().nlargest(n)
title = f"Les {n} sources les plus fréquentes"
bar_chart_figure = px.bar(top_sources, title=title)
src_distr_graph = html.Div(children=[
    dcc.Graph(
        id='src-distribution',
        figure=bar_chart_figure
    ),
])

tmp_df = pd.DataFrame()
tmp_df["source"] = df["src"].unique().copy()
tmp_df["source"] = tmp_df["source"].apply(lambda x: "humain" if "human" in x else "IA")
pie_proportion_graph = html.Div(children=[
    dcc.Graph(
        id='source-proportion',
        figure=px.pie(tmp_df, names='source', title='Proportion des sources (Humain vs IA)')
    ),
])

tmp_df = pd.DataFrame()
text_human = ' '.join(df[df["label"] == 1]["text"])
wordcloud_human = WordCloud(width=600, height=400, background_color='white').generate(text_human)

wordcloud_img = io.BytesIO()
wordcloud_human.to_image().save(wordcloud_img, format='PNG')
wordcloud_human_base64 = base64.b64encode(wordcloud_img.getvalue()).decode('utf-8')

word_cloud_human = html.Div(children=[
    html.Img(src=f'data:image/png;base64,{wordcloud_human_base64}', title='Nuage de mots les plus répandus (humains)')
])

tmp_df = pd.DataFrame()
text_ia = ' '.join(df[df["label"] == 0]["text"])
wordcloud_ia = WordCloud(width=600, height=400, background_color='white').generate(text_ia)

wordcloud_img = io.BytesIO()
wordcloud_ia.to_image().save(wordcloud_img, format='PNG')
wordcloud_ia_base64 = base64.b64encode(wordcloud_img.getvalue()).decode('utf-8')

word_cloud_ia = html.Div(children=[
    html.Img(src=f'data:image/png;base64,{wordcloud_ia_base64}', title='Nuage de mots les plus répandus (IAs)')
])

#### OLD DATAFRAME ####

# old_df = get_dataframe()

#### LAYOUT ####

app.layout = html.Div([
    # Div Titre
    html.Div(children=[  # TODO
        html.H1(children='IA vs AI : Tableau de bord de visualisation des données'),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'}),

    # Div Haute
    html.Div(children=[
        html.Div(children=[
            pie_graph
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            text_len_graph
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            src_distr_graph
        ], style={'padding': 10, 'flex': 1}),

    ], style={'display': 'flex', 'flexDirection': 'row', 'padding': '5% 0'}),

    # Div Milieu
    html.Div(children=[
        html.Div(children=[
            pie_proportion_graph
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            html.H5(children='Nuages de mots les plus courants (humains)'),
            word_cloud_human
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[
            html.H5(children='Nuages de mots les plus courants (IAs)'),
            word_cloud_ia
        ], style={'padding': 10, 'flex': 1}),

    ], style={'display': 'flex', 'flexDirection': 'row', 'padding': '5% 0'}),
])

PORT = 5000
ADDRESS = "0.0.0.0"
if __name__ == '__main__':
    app.run_server(debug=False, port=PORT, host=ADDRESS)
