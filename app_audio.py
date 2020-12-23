import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import librosa
import librosa.display
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64
import io 
from utils import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

n_fft = 256

audio_file = "assets/voice1.mp3"
t, v_signal1, fs1 = load_audio(audio_file)
encoded_image1 = stft_save_image(v_signal1, n_fft, fs1, "assets/img1")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=t, y=v_signal1, mode="lines"))

audio_file2 = "assets/voice2.mp3"
t, v_signal2, fs2 = load_audio(audio_file)
encoded_image2 = stft_save_image(v_signal2, n_fft, fs2, "assets/img2")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=t, y=v_signal2, mode="lines"))


upload_data_style = {
    'width': '100%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin-bottom': '20px'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Upload(
        id="upload-audio",
        children=html.Div([
            "Drag and Drop or ",
            html.A("Select Files")
        ]),
        style=upload_data_style
    ),
    dcc.Upload(
        id="upload-audio-2",
        children=html.Div([
            "Drag and Drop or ",
            html.A("Select Files")
        ]),
        style=upload_data_style
    ),
    html.Audio(src=audio_file, controls=True),
    html.Audio(src=audio_file2, controls=True),
    # html.Audio(src=audio_file2, controls=True),
    dcc.Graph(id="audio-1", figure=fig1),
    dcc.Graph(id="audio-2", figure=fig2),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image1), className="img1"),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image2), className="img2")
])


if __name__ == '__main__':
    app.run_server(debug=True)