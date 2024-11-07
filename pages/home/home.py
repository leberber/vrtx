
from dash import register_page
import dash_mantine_components as dmc
from dash import dcc
register_page(__name__, path="/home")



layout = dmc.Box(
    p='10px 40px',
    children = [
     'Home'
    ]
)

# box-shadow: ;