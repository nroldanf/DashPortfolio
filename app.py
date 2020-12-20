import os
import base64
from utils import *

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

image_filename = 'emanon.jpg' # replace with your own image
with open(image_filename, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode('ascii')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    dcc.Upload(
        id="upload-data",
        children=html.Div([
            "Drag and Drop or ",
            html.A("Select Files")
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
    html.Div(id="output-data-upload")
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def update_output(content):
    if content is not None:
        # with open("content_callback", "w") as f:
        #     f.write(content)
        # data:tipo;base64
        children = [html.Img(src=content)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)