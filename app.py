
from dash import (
    Dash, html, ALL, dcc, callback, Input, Output, State, 
    clientside_callback, ClientsideFunction,
    _dash_renderer, page_registry, page_container, no_update, set_props
)
from flask import Flask, request, redirect, session, url_for
import json, os
import dash_mantine_components as dmc

# Internal Imports
from components.sidebar import sidebar
from utils.helpers import iconify
from appconfig import stylesheets

_dash_renderer._set_react_version("18.2.0")


# server = Flask(__name__)
# server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))

app = Dash(
    __name__,  use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=stylesheets,
)

# server = app.server

# oauth = OAuth(server)


sidebar = dmc.Box(
    children = [
         dmc.NavLink(
            label="Home",
            leftSection=iconify(icon="solar:home-2-line-duotone", width = 20),
            href='/'
        ),
        dmc.NavLink(
            label="Autodrafter",
            leftSection=iconify(icon="hugeicons:analytics-02", width = 20),
            href='/autodrafter'
        ),
        dmc.NavLink(
            label="Secret",
            leftSection=iconify(icon="solar:lock-keyhole-minimalistic-unlocked-line-duotone", width = 20),
            href='/secret'
        ),
    ]
)

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    children=[
        dmc.Box(
            sidebar, 
            id='sidebar', 
        ),
        dmc.Box(
            id='container',
            pos = 'relative',
            children = [
                dmc.Box(
                    w = '100%',
                    h = '9%',
                    pt = 20,
                    pb =10,
                    pos = 'relative',
                    style = { 
                        'zIndex':'1000',
                        'boxShadow': 'rgba(27, 31, 35, 0.04) 0px 1px 0px, rgba(255, 255, 255, 0.25) 0px 1px 0px inset'
                    },
                    children = [
                        dmc.ActionIcon(
                            style = {'position':'absolute', 'left':'5px', 'top':'73%', "transform": "translateY(-50%)" },   
                            size="md",
                            variant = 'subtle',
                            id="hide-show-side-bar",
                            color='gray',
                            n_clicks=0,
                            children = iconify(icon = 'hugeicons:menu-02')
                        ),
                        dmc.Box(
                                style = {'position':'absolute', 'left':'25px', 'top':'60%', "transform": "translateY(-50%)" }, 
                                children = [
                                    dmc.Image(
                                        ml ='-5px',
                                        src="/assets/logo.svg",
                                        fit='contain',
                                        h ='60px',
                                        mr= '40px',
                                    ),
                                ]
                            ),
                        dmc.Group(
                            gap = 5,
                            style = {'position':'absolute', 'right':'20px','bottom':'6px'},
                            children=[
                                dmc.Avatar(
                                    src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes"
                                    "-computer-wallpaper-thumbnail.png",
                                    size="md",
                                    radius="xl",
                                ),
                                dmc.Box(
                                    children = [
                                        dmc.Text('John Doe', fw = 'bold', lh = 1.2),
                                        dmc.Text('john.doe@vrtx.com', c='gray', size='sm', lh=1.2),
                                    ]
                                ),
                                    dmc.SegmentedControl(
                                    id="color-scheme-toggle",
                                    value="Light",
                                    size = 'xs',
                                    radius = 15,
                                    px = 10,
                                    ml = 30,
                                    mt = 10,
                                    data=[
                                        {
                                            "value": 'Light',
                                            "label": dmc.Center(
                                                [iconify(icon='ic:baseline-light-mode', width=16), html.Span('Light', style = {"paddingRight":"10px"})],
                                                style={"gap": 10},
                                            )
                                        },
                                            {
                                            "value": 'Dark',
                                            "label": dmc.Center(
                                                [iconify(icon='ic:sharp-dark-mode', width=16), html.Span('Dark', style = {"paddingRight":"10px"})],
                                                style={"gap": 10},
                                            )
                                        }
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dmc.Box(
                    h='91%',
                    style = { "overflow": "scroll" },
                    children = [
                        page_container
                    ]
                )
            ]
        )
    ]
)


clientside_callback(
    ClientsideFunction(
        namespace='theme',
        function_name='theme_switcher_callback'
    ),
    Output("mantine-provider", "theme"),
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "value")
)

clientside_callback(
    ClientsideFunction(
        namespace='helpers',
        function_name='hide_show_sidebar'
    ),
Output("sidebar", "style"),
Output("container", "style"),
Input("hide-show-side-bar", "n_clicks")
)

if __name__ == "__main__":
    app.run_server(
        debug=True,
        port= 8051
    )

