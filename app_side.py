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
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

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

    
button_nav = three_lines_button()


page_content_face = [
    html.H2('Face Verification API', style={"margin": 20}),
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
    dbc.Row([
        dbc.Col(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
                style={'margin': 50},
                id="output-data-upload"
            )
        ),
        dbc.Col(
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
                style={'margin': 50},
                id="output-data-upload-2"
            )
        )
    ])
]

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
    style={"background-color": "black"}
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        # html.Div(
        #     [
        #         html.Hr(),
        #     ],
        #     id="blurb",
        # ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Face Verification", href="/face-verification", active="exact"),
                    dbc.NavLink("Voice Verification", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
                style={
                    "background-color": "black",
                    "color": "white"
                }
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/face-verification":
        return page_content_face
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


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
    app.run_server(port=8888, debug=True)