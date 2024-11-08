from dash import html, dcc, Output, Input, State, MATCH, ALL, Patch, ctx, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd

import base64
from utils.helpers import iconify

from pages.autodrafter.language import DCT_DF

NUM_COLS = 3


# Add Row Button Clicked -> Add Row
def make_row(row_number):
    vendors = DCT_DF["Vendor"].unique()
    vendor_dropdown = dmc.Select(
        data=vendors,
        mx =7, my=3,
        id={"type": "vendor_dropdown", "index": row_number},
        placeholder="Select a Vendor",
        value=None,
    )

    product_dropdown = dmc.Select(
        data=[],
        mx =7, my=3,
        id={"type": "product_dropdown", "index": row_number},
        placeholder="Select a Product",
        disabled=True,
        value=None,
    )

    consent_dropdown = dmc.Select(
        data=[],
        mx =7, my=3,
        id={"type": "consent_dropdown", "index": row_number},
        placeholder="Select Consent Language",
        disabled=True,
        value=None,
    )

    remove_button = dmc.Button(
            "Remove",
            variant="subtle",
            id={"type": "remove_button", "index": row_number}, 
            leftSection=iconify(icon="simple-line-icons:minus", width = 20),
            color="vp",
        ),


    return html.Tr(
        [
            html.Td(vendor_dropdown),
            html.Td(product_dropdown),
            html.Td(consent_dropdown),
            html.Td(remove_button),
        ],
        id={"type": "table_row", "index": row_number},
    )


dct_layout = dmc.Box(
            # pt = 40,
            pb = 30,
            children = [
                dmc.Box(
                    children = [
                        dmc.Table(
          # horizontalSpacing= 80,
                            verticalSpacing = 0,
                            styles= {
                                'thead':{'border':'none'},
                                'tr':{'border':'none'},
                            },
                            children =[
                                dmc.TableThead(
                                    dmc.TableTr(
                                        [
                                            dmc.TableTh("Vendor"),
                                            dmc.TableTh("Product"),
                                            dmc.TableTh("Consent Language"),
                                        ]
                                    )
                                ),
                                dmc.TableTbody(
                                    children=[
                                        make_row(1),
                                        make_row(2),
                                    ],
                                    id="dct_table_body",
                                ),
                            ],
                            id="dct_table",
                        ),
                        dmc.Grid(
                            [
                                dmc.GridCol(
                                    dmc.Button(
                                        "Add Row", 
                                        id="add_row_button", 
                                        n_clicks=4,
                                        variant="subtle",
                                        leftSection=iconify(icon="simple-line-icons:plus", width =20),
                                        color="vp",
                                    )
                                )
                            ]
                        ),
                    ],
                ),
            ]
        )

# Open Modal
@callback(
    Output("dct_modal", "is_open"),
    [
        Input("dct_button", "n_clicks"),
        Input("dct_modal_close", "n_clicks"),
    ],
    [State("dct_modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_modal( btn,_, is_open):
    return not is_open


@callback(
    Output("dct_table_body", "children"),
    [Input("add_row_button", "n_clicks")],
    Input({"type": "remove_button", "index": ALL}, "n_clicks"),
    [State("dct_table_body", "children")],
    prevent_initial_call=True,
)
def add_delete_row(n_clicks, _, children):
    if ctx.triggered_id == "add_row_button" or not ctx.triggered_id:
        children.append(make_row(n_clicks))
    else:
        delete_index = ctx.triggered_id["index"]
        children = [
            elem for elem in children if elem["props"]["id"]["index"] != delete_index
        ]
    return children


# Vendor Selected
@callback(
    Output({"type": "product_dropdown", "index": MATCH}, "data"),
    Output({"type": "product_dropdown", "index": MATCH}, "disabled"),
    Input({"type": "vendor_dropdown", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def vendor_clicked(vendor_value):
    product_df = DCT_DF[DCT_DF["Vendor"] == vendor_value]
    products = product_df["ICF Topic"].unique()
    return products, len(products) == 0


# Vendor or Product Chosen
@callback(
    Output({"type": "consent_dropdown", "index": MATCH}, "data"),
    State({"type": "vendor_dropdown", "index": MATCH}, "value"),
    Input({"type": "product_dropdown", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def product_clicked(vendor_value, product_value):
    if vendor_value is None or product_value is None:
        return []
    unique_key = vendor_value + " - " + product_value
    df = DCT_DF.loc[unique_key]
    default_language = df.loc["Signature page; Consent - Mandatory/Default"]
    optional_language = df.loc["Consent - Optional"]

    return_list = []
    if default_language is not None and not pd.isnull(default_language):
        return_list.append("Default/Mandatory")
    if optional_language is not None and not pd.isnull(optional_language):
        return_list.append("Optional")

    return return_list


# Disable Consent if Options are length 0 (i.e. no vendor or product chosen)
@callback(
    Output({"type": "consent_dropdown", "index": MATCH}, "disabled"),
    Output({"type": "consent_dropdown", "index": MATCH}, "value"),
    Input({"type": "consent_dropdown", "index": MATCH}, "data"),
    prevent_initial_call=True,
)
def consent_populated(consent_options):
    return len(consent_options) == 0, "Default/Mandatory"


# Store data if modal is closed
@callback(
    Output("data_store", "data", allow_duplicate=True),
    Input("dct_modal", "is_open"),
    [State("dct_table_body", "children")],
    [State("data_store", "data")],
    prevent_initial_call=True,
)
def update_output(is_open, table, data):
    if not is_open:
        dct_dict = {}
        dct_dict["VENDORS"] = []
        dct_dict["VENDOR_APPS"] = []
        dct_dict["APP_DEFAULTS"] = []
        dct_dict["APP_OPTIONALS"] = []

        data_rows = [child["props"]["children"] for child in table]
        vendors = [elem[0]["props"]["children"]["props"]["value"] for elem in data_rows]
        products = [
            elem[1]["props"]["children"]["props"]["value"] for elem in data_rows
        ]
        consents = [
            elem[2]["props"]["children"]["props"]["value"] for elem in data_rows
        ]

        df = pd.DataFrame([vendors, products, consents]).T
        df.columns = ["VENDOR", "PRODUCT", "CONSENT"]
        df = df.dropna(axis=0, how="any")
        if len(df) > 0:
            df["VENDOR_PRODUCT"] = df["VENDOR"] + " - " + df["PRODUCT"]
            optional_df = df[
                df["CONSENT"] == "Signature page; Consent - Mandatory/Default"
            ]
            mandatory_df = df[df["CONSENT"] == "Optional"]

            dct_dict["VENDORS"] = df["VENDOR"].unique()
            dct_dict["VENDOR_APPS"] = df["VENDOR_PRODUCT"].unique()
            dct_dict["APP_DEFAULTS"] = mandatory_df["VENDOR_PRODUCT"].unique()
            dct_dict["APP_OPTIONALS"] = optional_df["VENDOR_PRODUCT"].unique()

            # dct_dict = replace_dct_choices(DCT_DF, dct_dict)
            data["dct"] = dct_dict
    return data