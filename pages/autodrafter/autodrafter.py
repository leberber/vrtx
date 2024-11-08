import pandas as pd
import base64
import subprocess
import os
from pathlib import Path
import uuid

from dash import  ( 
    Output, Input, callback, State, ctx, ALL, set_props, no_update,
    register_page, dcc, clientside_callback
)

import dash_mantine_components as dmc
from utils.helpers import iconify


from pages.autodrafter.formInputs import  form_progress, prepare_metadata
from pages.autodrafter.layout import makeAccordion, aside, bottomNavigation, preview_page

register_page(__name__, path="/")

df = pd.read_csv('metadata_updated.csv')

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
        # dmc.Box(dct_layout)
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
    Output("regenerate-button", "disabled"),
    Output("download-button", "disabled"),

    Input({"type": "forms-user-inputs", "index": ALL}, "value"),
    Input('document-uploader', 'contents'),
    Input('highlight', 'value'),
    
    State('document-uploader', 'filename'),
    State('app-front-end-store', 'data'),
    # prevent_initial_call =True
)
def progress_callbakcs(values, content, highlight, file_name, store):

    input_dict = {item['id']['index']: item['value'] for item in ctx.inputs_list[0]}
    store['user_inputs'] = input_dict
    store['uploded_docx_content'] = content
    store['highlight'] = highlight
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
        generate_button_state,
        generate_button_state
    ]


clientside_callback(
    """function updateLoadingState(n_clicks) {
    const no_update = window.dash_clientside.no_update
    if (!n_clicks){
        return no_update
    }
    return true
    }
    """,
    Output("generate-draft", "loading"),
    Input("generate-draft", "n_clicks"),
    prevent_intial_call = True
)

clientside_callback(
    """function openModalAndTriggerLoadding(n_clicks) {
    const no_update = window.dash_clientside.no_update
    if (!n_clicks){
        return no_update
    }
    return [true, true]
    }
    """,
    Output("loading-overlay", "visible"),
    Output("preview-pdf-modal", "opened"),
    Input("generate-draft", "n_clicks"),
    Input("regenerate-button", "n_clicks"),
    prevent_intial_call = True
)

@callback(
    Output("pdf-viewer", "data"),
    Input('generate-draft', 'n_clicks'),
    Input('regenerate-button', 'n_clicks'),
    State('app-front-end-store', 'data'),
    
    prevent_initial_call =True
)
def back_end_call(genarate, regenarate, store):
    import time
    time.sleep(10)

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
    set_props("loading-overlay", { "visible": False})
    set_props("generate-draft", { "loading": False})

    # store.pop("generated_docx_content", None)  # `None` avoids KeyError if key isn't found
    # store.pop("uploded_docx_content", None)
    # print(store)

    return f"data:application/pdf;base64,{pdf_base64}"
    
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
    State("preview-pdf-modal", "opened"),
    prevent_initial_call=True,
)
def func(n_clicks, opened):
    set_props("preview-pdf-modal", {'opened': not opened})

  









# @callback(
#     Output("dct_modal", "is_open"),
#     [
#         Input("dct_button", "n_clicks"),
#         Input("dct_modal_close", "n_clicks"),
#     ],
#     [State("dct_modal", "is_open")],
#     prevent_initial_call=True,
# )
# def toggle_modal( btn,_, is_open):
#     return not is_open


# @callback(
#     Output("dct_table_body", "children"),
#     [Input("add_row_button", "n_clicks")],
#     Input({"type": "remove_button", "index": ALL}, "n_clicks"),
#     [State("dct_table_body", "children")],
#     prevent_initial_call=True,
# )
# def add_delete_row(n_clicks, _, children):
#     if ctx.triggered_id == "add_row_button" or not ctx.triggered_id:
#         children.append(make_row(n_clicks))
#     else:
#         delete_index = ctx.triggered_id["index"]
#         children = [
#             elem for elem in children if elem["props"]["id"]["index"] != delete_index
#         ]
#     return children


# # Vendor Selected
# @callback(
#     Output({"type": "product_dropdown", "index": MATCH}, "options"),
#     Output({"type": "product_dropdown", "index": MATCH}, "disabled"),
#     Input({"type": "vendor_dropdown", "index": MATCH}, "value"),
#     prevent_initial_call=True,
# )
# def vendor_clicked(vendor_value):
#     product_df = DCT_DF[DCT_DF["Vendor"] == vendor_value]
#     products = product_df["ICF Topic"].unique()
#     return products, len(products) == 0


# # Vendor or Product Chosen
# @callback(
#     Output({"type": "consent_dropdown", "index": MATCH}, "options"),
#     State({"type": "vendor_dropdown", "index": MATCH}, "value"),
#     Input({"type": "product_dropdown", "index": MATCH}, "value"),
#     prevent_initial_call=True,
# )
# def product_clicked(vendor_value, product_value):
#     if vendor_value is None or product_value is None:
#         return []
#     unique_key = vendor_value + " - " + product_value
#     df = DCT_DF.loc[unique_key]
#     default_language = df.loc["Signature page; Consent - Mandatory/Default"]
#     optional_language = df.loc["Consent - Optional"]

#     return_list = []
#     if default_language is not None and not pd.isnull(default_language):
#         return_list.append("Default/Mandatory")
#     if optional_language is not None and not pd.isnull(optional_language):
#         return_list.append("Optional")

#     return return_list


# # Disable Consent if Options are length 0 (i.e. no vendor or product chosen)
# @callback(
#     Output({"type": "consent_dropdown", "index": MATCH}, "disabled"),
#     Output({"type": "consent_dropdown", "index": MATCH}, "value"),
#     Input({"type": "consent_dropdown", "index": MATCH}, "options"),
#     prevent_initial_call=True,
# )
# def consent_populated(consent_options):
#     return len(consent_options) == 0, "Default/Mandatory"


# # Store data if modal is closed
# @callback(
#     Output("data_store", "data", allow_duplicate=True),
#     Input("dct_modal", "is_open"),
#     [State("dct_table_body", "children")],
#     [State("data_store", "data")],
#     prevent_initial_call=True,
# )
# def update_output(is_open, table, data):
#     if not is_open:
#         dct_dict = {}
#         dct_dict["VENDORS"] = []
#         dct_dict["VENDOR_APPS"] = []
#         dct_dict["APP_DEFAULTS"] = []
#         dct_dict["APP_OPTIONALS"] = []

#         data_rows = [child["props"]["children"] for child in table]
#         vendors = [elem[0]["props"]["children"]["props"]["value"] for elem in data_rows]
#         products = [
#             elem[1]["props"]["children"]["props"]["value"] for elem in data_rows
#         ]
#         consents = [
#             elem[2]["props"]["children"]["props"]["value"] for elem in data_rows
#         ]

#         df = pd.DataFrame([vendors, products, consents]).T
#         df.columns = ["VENDOR", "PRODUCT", "CONSENT"]
#         df = df.dropna(axis=0, how="any")
#         if len(df) > 0:
#             df["VENDOR_PRODUCT"] = df["VENDOR"] + " - " + df["PRODUCT"]
#             optional_df = df[
#                 df["CONSENT"] == "Signature page; Consent - Mandatory/Default"
#             ]
#             mandatory_df = df[df["CONSENT"] == "Optional"]

#             dct_dict["VENDORS"] = df["VENDOR"].unique()
#             dct_dict["VENDOR_APPS"] = df["VENDOR_PRODUCT"].unique()
#             dct_dict["APP_DEFAULTS"] = mandatory_df["VENDOR_PRODUCT"].unique()
#             dct_dict["APP_OPTIONALS"] = optional_df["VENDOR_PRODUCT"].unique()

#             # dct_dict = replace_dct_choices(DCT_DF, dct_dict)
#             data["dct"] = dct_dict
#     return data