import pandas as pd
import base64
import subprocess
import os
from pathlib import Path
import uuid

from dash import  ( 
    Output, Input, callback, State, ctx, ALL, set_props, no_update,
    register_page, dcc
)

import dash_mantine_components as dmc
from utils.helpers import iconify


from pages.autodrafter.formInputs import  form_progress, prepare_metadata
from pages.autodrafter.layout import makeAccordion, aside, bottomNavigation, preview_page

register_page(__name__, path="/")

df = pd.read_csv('metadata.csv')

metadata= prepare_metadata(df)

layout = dmc.Box(
    mr = 350,
    ml = 70,
    pos='relative !important',
    children = [
        dcc.Store(
            id='app-front-end-store', 
            data = {}
        ),
        dcc.Download(id='download-word-docx'),
        dmc.Text('Vertex ICF Autodrafter Pilot', 
            variant="gradient",
            mt=20,
            fw='bold',
            ta='center',
            gradient={"from": "#52247f", "to": "#00A7B5", "deg":0},
            style={"fontSize": 40},
        ),
        preview_page,
        makeAccordion(metadata),
        aside,
        bottomNavigation,
    ]
)

@callback(
    Output({"type": "step-percent-label", "index": ALL}, "children"),
    Output({"type": "step-percent-progress", "index": ALL}, "value"),
    Output({"type": "step-percent-progress", "index": ALL}, "color"),
    Output({"type": "step-icon-progress", "index": ALL}, "children"),
    Output({"type": "step-icon-progress", "index": ALL}, "color"),
    Output("ring-progress-total-label", "children"),
    Output("ring-progress-total-value", "sections"),
    Output("upload-step-percent-label", "children"),
    Output("upload-step-percent-progress",  "value"),
    Output("upload-step-icon-progress", "children"),
    Output("upload-step-icon-progress", "color"),
    Output("upload-step-percent-progress", "color"),
    Output("upload-content-area", "bg"),
    Output("name-of-uploaded-file", "children"),
    Output("generate-draft", "disabled"),
    Output("download-button", "disabled"),

    Input({"type": "forms-user-inputs", "index": ALL}, "value"),
    Input('document-uploader', 'contents'),
    State('document-uploader', 'filename'),
    State('app-front-end-store', 'data'),
    # prevent_initial_call =True
)
def progress_callbakcs(values, content, file_name, store):

    input_dict = {item['id']['index']: item['value'] for item in ctx.inputs_list[0]}
    store['user_inputs'] = input_dict
    store['uploded_docx_content'] = content
    set_props("app-front-end-store", {'data': store})

    d = list(form_progress(input_dict).values())
    text_labels = [f"{int(100-i)}%" for i in d]
    content_percent = 100 if content else 0

    progress = [int(100-i) for i in d]
    progress_all = [int(100-i) for i in d] + [content_percent]
    total = int(sum(progress_all)/len(progress_all))
    
    total_color='red' if total !=100 else 'green'
    total_icon= f"{total}%" if total !=100 else iconify('lets-icons:done-duotone', color='green', width = 60)

    icons = [
        iconify('lets-icons:done-duotone', color='green') 
        if icon ==100 
        else iconify('material-symbols-light:wifi-tethering-rounded', rotate=3) 
        for icon in progress  
    ]

    colors = ['green' if icon ==100 else 'red' for icon in progress  ]

    
    upload_progress_label ='0%' if not content else '100%'
    upload_progress_value = 0 if not content else 100

    upload_bg= 'rgba(64, 192, 87, 0.1)' if content else 'none'
    name_file = file_name if file_name else 'Drag and drop files here to upload.'
    generate_button_state = True  if total !=100 else False
    
   
    upload_progress_icon =iconify('material-symbols-light:wifi-tethering-rounded', rotate=3) if not content else iconify('lets-icons:done-duotone', color='green') 
    upload_progress_color ='red' if not content else 'green'
    total_progress = [{'value': total, 'color': total_color}]

    return [
        text_labels, 
        progress, 
        colors, 
        icons, 
        colors, 
        total_icon, 
        total_progress,
        upload_progress_label ,
        upload_progress_value ,
        upload_progress_icon,
        upload_progress_color,
        upload_progress_color,
        upload_bg,
        name_file,
        generate_button_state,
        generate_button_state
    ]

@callback(
    Output("pdf-viewer", "data"),
    Output("preview-pdf-modal", "opened"),
    Input('generate-draft', 'n_clicks'),
    State('app-front-end-store', 'data'),
    State("preview-pdf-modal", "opened"),
    prevent_initial_call =True
)
def update_user_initials(genarate, store, opened):

    # return f"", True

    def convert_word_to_pdf(input_path):
        command = [
            "soffice", "--headless", "--convert-to", "pdf", "--outdir",
            os.path.dirname(input_path), input_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode 

    # HERE WE MAKE A CALL TO GENEREATE THE WORD DOCX
    #   ******************************************
    #   ******************************************
    #   ******************************************
    #                   END
    store['generated_docx_content'] = store['uploded_docx_content']
    set_props("app-front-end-store", {'data': store})

    wordContent = store['generated_docx_content'] 
    uuid_file_name = str(uuid.uuid1())

    _, content_string = wordContent.split(',')
    decoded = base64.b64decode(content_string)

    with open(f'{uuid_file_name}.docx', 'wb') as f:
        f.write(decoded)
        
    convert_word_to_pdf(f'{uuid_file_name}.docx')

    pdf_bytes = Path(f'{uuid_file_name}.pdf').read_bytes()

    os.remove(f"{uuid_file_name}.docx")
    os.remove(f"{uuid_file_name}.pdf")

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    return f"data:application/pdf;base64,{pdf_base64}", True
    


@callback(
    Output("download-word-docx", "data"),
    Input("download-button", "n_clicks"),
    State("app-front-end-store", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, store):
    if not store.get('generated_docx_content'):
        return no_update
    wordContent = store['generated_docx_content'] 
    _, content_string = wordContent.split(',')
    contents = base64.b64decode(content_string)
    return dcc.send_bytes(contents, f"autodrafted_icf.docx")

@callback(
    Input("preview-draft", "n_clicks"),
    # State("app-front-end-store", "data"),
    State("preview-pdf-modal", "opened"),
    prevent_initial_call=True,
)
def func(n_clicks, opened):
    set_props("preview-pdf-modal", {'opened': not opened})

  

