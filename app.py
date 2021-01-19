"""
This app creates a collapsible, responsive sidebar layout with
dash-bootstrap-components and some custom css with media queries.
When the screen is small, the sidebar moved to the top of the page, and the
links get hidden in a collapse element. We use a callback to toggle the
collapse when on a small screen, and the custom CSS to hide the toggle, and
force the collapse to stay open when the screen is large.
dcc.Location is used to track the current location, a callback uses the current
location to render the appropriate page content. The active prop of each
NavLink is set automatically according to the current pathname. To use this
feature you must install dash-bootstrap-components >= 0.11.0.
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import os
import base64
from utils import *

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

server = app.server


image_filename = 'emanon.jpg' # replace with your own image
with open(image_filename, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode('ascii')


def three_lines_button():
    div_component = html.Div(style={
        "width": 35,
        "height": 5,
        "background-color": "white",
        "marginTop": 5,
        "marginBottom": 5
    })
    butt_component = html.Div([
        div_component,
        div_component,
        div_component
    ])
    return butt_component

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "black",
    "color": "white"
}
    
button_nav = three_lines_button()

# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    # html.Span(className="navbar-toggler-icon"),
                    button_nav,
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "border-color": "rgba(255,255,255,.6)",
                        'marginBottom': 20,
                        'marginTop': 20,
                        'marginLeft': 20
                    },
                    id="navbar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        )
    ],
    style={"background-color": "black"},
    className="sidebar"
)

sidebar = html.Div(
    [
        sidebar_header,
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Face Verification", href="/face-verification", active="exact")
                ],
                vertical=True,
                pills=True,
                style={
                    "background-color": "black",
                    "color": "white"
                }
            ),
            id="collapse"
        ),
    ],
    id="sidebar"
)


simple_sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Face Verification", href="/face-verification", active="exact")
            ],
            vertical=True,
            pills=False,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="simplesidebar"
)


images_component =  dbc.Row(
    [
        dbc.Col(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image), className="img"),
                id="output-data-upload",
                className="img-div"
            ),
            width=5
        ),
        dbc.Col(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image), className="img"),
                id="output-data-upload-2",
                className="img-div"
            ),
            width=5
        ),
    ], justify="center", className="images-component")


images_component_cell = dbc.Row([
    dbc.Col(html.Div([
        dbc.Row(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image), className="img"),
                style={'margin': 50},
                id="output-data-upload-c"
            )
        ),
        dbc.Row(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image), className="img"),
                style={'margin': 50},
                id="output-data-upload-c-2"
            )
        )
    ]))
], justify="center", className="images-component-cell")


page_content_face = [
    dbc.Container([
        html.Div([
            dbc.Row([
                dbc.Col(simple_sidebar, width={"size":2}, className="simplesidebar"),
                dbc.Col([
                    dbc.Row([
                        html.Div([
                            html.H2('Face Verification API', style={"margin": 20}),
                            html.Hr()
                        ], style={"text-align": "center"})
                        
                    ], justify="center"),
                    dbc.Row([
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
                                'margin-bottom': '20px'
                            }
                        ),
                    ], justify="center"),
                    images_component,
                    images_component_cell,
                    dbc.Card([
                        dbc.CardHeader("Similarity Porcentage: {}".format(90), style={"color": "white", "text-align": "center", "font-size": "20px"}, id="similarity-result"),
                        dbc.CardBody([
                            dbc.Button("Get Similarity", color="dark", style={"margin-top": "20px", "margin-bottom": "20px"}, block=True)
                        ]),
                    ], style={"margin-top": "20px", "margin-bottom": "20px"}, color="secondary")
                ])
            ])
        ])
    ],
    fluid=True)
]

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return page_content_face
    elif pathname == "/face-verification":
        return page_content_face
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def update_output(content):
    if content is not None:
        # with open("content_callback", "w") as f:
        #     f.write(content)
        # data:tipo;base64
        children = [html.Img(src=content, className="img")]
        return children
    else:
        return [html.Img(src='data:image/png;base64,{}'.format(encoded_image), className="img")]



@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
# import os
# import base64
# from utils import *

# import dash
# from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# image_filename = 'emanon.jpg' # replace with your own image
# with open(image_filename, 'rb') as f:
#     encoded_image = base64.b64encode(f.read()).decode('ascii')

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# server = app.server


# app.layout = html.Div([
#     html.H2('Hello World'),
#     dcc.Dropdown(
#         id='dropdown',
#         options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
#         value='LA'
#     ),
#     dcc.Upload(
#         id="upload-data",
#         children=html.Div([
#             "Drag and Drop or ",
#             html.A("Select Files")
#         ]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         }
#     ),
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
#     html.Div(id="output-data-upload")
# ])

# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)


# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload-data', 'contents'))
# def update_output(content):
#     if content is not None:
#         # with open("content_callback", "w") as f:
#         #     f.write(content)
#         # data:tipo;base64
#         children = [html.Img(src=content)]
#         return children


# if __name__ == '__main__':
#     app.run_server(debug=True)