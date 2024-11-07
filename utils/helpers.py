
from dash_iconify import DashIconify
def iconify(icon, color = 'dark', width=30, cN = '_', rotate=None):
    return DashIconify(
        icon=icon,  
        color=color, 
        width = width, 
        rotate=rotate,
        className=cN
    )

