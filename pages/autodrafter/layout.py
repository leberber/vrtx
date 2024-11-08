import dash_mantine_components as dmc
from utils.helpers import iconify
from dash  import dcc
import dash_pdf
from pages.autodrafter.formInputs import make_questions


def makeAccordion(metadata):
    steps = list(metadata.values())
    accordionItems =[
        dmc.AccordionItem(
            value='upload',
            children = [
                dmc.AccordionControl(
                    pos = 'relative',
                    icon=iconify(
                        icon="cuida:upload-outline",
                        color='rgba(0, 167, 181, 1)',
                        width=30
                    ),
                    children=[
                        dmc.Text(
                            'Upload Word Document', 
                            size="md", 
                            fw=900, 
                            lh=2
                        ),
                        dmc.Text(
                            'This step allow you to uplad a word document to generate a draft', 
                            size="sm", 
                            fw=400, 
                            c="dimmed",  
                            w = '70%'
                        ),
                        dmc.Box(
                            w = '15%',
                            m = 5,
                            style = {'position':'absolute', 'right':'5px', 'top':'0'},
                            children = [
                                dmc.Flex(
                                    align='flex-end',
                                    gap=5,
                                    children = [
                                        dmc.ActionIcon( 
                                            id="upload-step-icon-progress", 
                                            variant="light", 
                                            radius=50, 
                                            size=40, 
                                            color='green',
                                            style = { "transform": "translateY(20%)" }
                                        ),
                                        dmc.Box(
                                            children = [
                                                dmc.Group(
                                                    gap = 5,
                                                    children = [
                                                        dmc.Text(
                                                            '0%',
                                                            fw='bold',  
                                                            size = 'lg',  
                                                            id='upload-step-percent-label'
                                                        ), 
                                                        dmc.Text(
                                                            'Complete',  
                                                            size = 'sm', 
                                                            c = 'gray'
                                                        )
                                                    ]
                                                ),
                                                dmc.Progress(
                                                    value=0, 
                                                    size="xs", 
                                                    radius = 20, 
                                                    id="upload-step-percent-progress" 
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dmc.AccordionPanel(
                    dmc.Center(
                        # pt = 40,
                        pb = 30,
                        children = [
                            dcc.Upload(
                                style = {
                                    'border': '1px dashed rgb(206, 212, 218)',  
                                    'borderRadius': '5px', 
                                },
                                id='document-uploader',
                                children=dmc.Stack(
                                    id='upload-content-area', 
                                    miw=900,
                                   m = 15,
                                    align='center',
                                    style = {'padding': '1rem 1rem 3.125rem'},
                                    children=[
                                        iconify(
                                            'fa6-solid:upload', 
                                            width = 60, 
                                            color = '#492869'
                                        ),
                                        dmc.Text(
                                            'Drag and drop files here to upload.', 
                                            className='upload-text', 
                                            
                                            id='name-of-uploaded-file'
                                        ),
                                        dmc.Button(
                                            "Select File",
                                            color='vp',
                                            style = {
                                                'position': 'absolute', 
                                                'bottom': '-1.2rem', 'width': '15.625rem'
                                            },
                                            id='upload-button',
                                            radius='lg',
                                        )
                                    ]
                                )
                            ) 
                        ]
                    )
                )
            ]
        )
    ]

    for step in steps:
        accordionItems.append(
            dmc.AccordionItem(
                value=step['stepID'],
                children = [
                    dmc.AccordionControl(
                        pos = 'relative',
                        icon=iconify(
                            icon=step['stepIcon'],
                            color='rgba(0, 167, 181, 1)',
                            width=30
                        ),
                        children=[   
                            dmc.Text(step['stepName'], size="md", fw=900, lh=2),
                            dmc.Text(step['stepDescription'], size="sm", fw=400, c="dimmed",  w = '70%'),
                            dmc.Box(
                                w = '15%',
                                m = 5,
                                style = {'position':'absolute', 'right':'5px', 'top':'0' },
                                children = [
                                    dmc.Flex(
                                        align='flex-end',
                                        gap=5,
                                        children = [
                                            dmc.ActionIcon( 
                                                id={
                                                    'type':'step-icon-progress', 
                                                    'index':step['stepID']
                                                }, 
                                                variant="light", 
                                                radius=50, 
                                                size=40, 
                                                color='green',
                                                style = { "transform": "translateY(20%)" }
                                            ),
                                            dmc.Box(
                                                children = [
                                                    dmc.Group(
                                                        gap = 5, 
                                                        children = [
                                                            dmc.Text(
                                                                '0%',
                                                                fw='bold',  
                                                                size = 'lg',  
                                                                id={
                                                                    'type':'step-percent-label', 
                                                                    'index':step['stepID']
                                                                }
                                                            ), 
                                                            dmc.Text(
                                                                'Complete',  
                                                                size = 'sm', 
                                                                c = 'gray'
                                                            )
                                                        ]
                                                    ),
                                                    dmc.Progress(
                                                        value=0, 
                                                        size="xs", 
                                                        radius = 20, 
                                                        id={
                                                            'type':'step-percent-progress', 
                                                            'index':step['stepID']
                                                        } 
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    dmc.AccordionPanel(
                        children = make_questions (step) 
                    )
                ]
            )
        )

    return dmc.Accordion(
        pt = '10px',
        pb = '20px',
        chevron = None,
        id='checkbox-filters-accordion',
        styles = {
            'item':{
                'margin':8,
                "boxShadow":"rgba(0, 0, 0, 0.1) 0px 1px 2px 1px",
                'backgroundColor':'transparent',
            }
        },
        radius = 'md',
        variant = "separated", 
        style = { 'overflow': 'Scroll', 'height': '90%'},
        value = 'upload',
        children=accordionItems
    )

aside = dmc.Box(
    style = {
        "position": "absolute",
        "borderRadius": "10px",
        "top":'22%',
        "bottom":40,
        "right":20,
        "boxShadow":"rgba(0, 0, 0, 0.04) 0px 3px 5px"
    },
    w = 300, 
    children = [
        dmc.Center(
            w = '100%',
            h = 180,
            children = [
            dmc.RingProgress(
                roundCaps = True,
                size = 200,
                thickness=15,
                id="ring-progress-total-value",
                sections=[{"value": 0, "color": "indigo"}],
                label=dmc.Stack(
                    gap = 0,
                    align='center',
                    children=[
                        dmc.Text(
                            id="ring-progress-total-label", 
                            ta="center", 
                            fw='bold', 
                            style={"fontSize": 32}, mb= '-15px'
                            ),
                        dmc.Text('Complete',  size = 'sm', c = 'gray'),
                        ]
                    )
                )
            ]
        ),
            dmc.Text(
            "Total Progress",
            variant="gradient",
            gradient={"from": "#52247f", "to": "#00A7B5", "deg":0},
            fw=700,
            style={"fontSize": 24},
            ta='center'
        )
    ]
)
highlight =  dmc.Group(
    pos='absolute', bottom=20, right='10', p =10,
    style = {  
        "boxShadow":"rgba(82, 36, 127, 0.1) 0px 4px 10px",
        "borderRadius":"10px"
    },
    children = [
        dmc.Text("Highlight"),
        dmc.SegmentedControl(
            id = 'highlight',
            value="OFF",
            size = 'xs',
            radius = 15,
            px = 10,
  
            data=[
                {
                    "value": 'OFF',
                    "label": "OFF"
                },
                {
                    "value": 'ON',
                    "label": "ON"
                }
            ]
        )
    ]
)
bottomNavigation = dmc.Center(
    className='theme-background',
    opacity=1,
    pos='absolute', bottom=20, right='50%', w=320, h=60,
    style = {
        "boxShadow":"rgba(82, 36, 127, 0.1) 0px 4px 10px",
        "borderRadius":"10px",
        "transform": "translateX(18%)",
        "zIndex":20000,
        "opacity":1,
        },
    children=[
        dmc.Button(
            "Preview",    
            variant="outline", 
            leftSection=iconify(icon="icon-park-outline:preview-open", width=20), 
            styles={'label':{'fontSize':'18px'}, 'section':{'margin':2}}, 
            id='preview-draft', 
            color='blue', 
            mr=20,  
            size="sm"
        ),
        dmc.Button(
            "Generate",  
            leftSection=iconify(icon="uis:process", width=20),  
            styles={'label':{'fontSize':'18px'}, 'section':{'margin':2}},
            id='generate-draft', 
            color='green', 
            size="sm"
        ),  
    ]
)

preview_page =  dmc.Modal(
    id="preview-pdf-modal",
    styles={
        'header':{'minHeight':0, 'minHeight':0, 'padding':0},
        'close':{'position':'absolute', 'left':10, 'top':10, 'width':70, 'height':30}
    },
    centered=True,
    fullScreen=True,
    zIndex = 200000,
    closeButtonProps = {
        'icon':iconify('eva:arrow-back-outline', width=25 ),
        'children':   dmc.Text('Back', size= 'lg')
    },
    children=[
        dmc.Box(
            pt= 20,
            pos = 'absolute',
            top= 0, right=0, bottom=0, left=0,
            h = '100%',
            style= {"textAlign":"center"},
            children = [
                dmc.Center(
                    h = 'calc(100% - 100px)',
                    p = 0,
                    mx='25%',
                    
                    # style={'border':'2px solid red'},
                    children = [
                    dmc.LoadingOverlay(
                        visible=False,
                        id="loading-overlay",
                        overlayProps={"radius": "sm", "blur": 0.1},
                        loaderProps={
                        "variant": "custom",
                        "children": dmc.Image(
                            h=150,
                            radius="md",
                            src="/assets/Loader.gif",
                        ),
                    },
                        zIndex=10,
                    ),
                        dash_pdf.PDF(
                            id='pdf-viewer',
                            data='',
                            buttonClassName="pdf-pagination-buttons",
                            labelClassName="pdf-pagination-label",
                            controlsClassName="pdf-pagination-controls",
                        )
                    ]
                ),
                dmc.Button(
                    "Download",
                    pos = 'absolute',
                    right='calc(50% - 177px)', 
                    bottom=20, 
                    variant="outline",
                    id ='download-button',
                    leftSection=iconify(
                        icon="solar:download-minimalistic-linear", 
                        width= 20
                    )
                ),
                dmc.Button(
                    "Re-Generate",
                    pos = 'absolute',
                    right='calc(50% - 350px)', 
                    styles={'label':{'fontSize':'18px'}, 'section':{'margin':2}},
                    bottom=20, 
                    color='green', 
                    size="sm",
                    id ='regenerate-button',
                    leftSection=iconify(icon="uis:process", width=20), 
                )
            ]
        )
    ]
)