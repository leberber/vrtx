import pandas as pd



def get_ta_df(path):
    df = pd.read_excel(
        path,
        sheet_name="TA Specific",
        dtype=str,
    )
    df["TA"] = df["TA"].map(
        lambda x: None if pd.isnull(x) or x.strip() == "" else x.strip()
    )
    df["Subcategory"] = df["Subcategory"].map(
        lambda x: None if pd.isnull(x) or x.strip() == "" else x.strip()
    )
    df["Subcategory"] = df["Subcategory"].fillna("All").astype(str)
    return df


def get_ll_procedures_df(path):
    ll_mapping = {
        "study procedures": "study_assessments_general",
        "procedural risks": "procedure_risks",
    }

    ll_procedures_df = pd.read_excel(path, sheet_name="Study Procedures", dtype=str)
    ll_procedures_df.columns = ll_procedures_df.columns.map(lambda x: x.strip())

    ll_procedures_df["TA"] = ll_procedures_df["TA"].map(
        lambda x: None if pd.isnull(x) or x.strip() == "" else x.strip()
    )
    ll_procedures_df["Subcategory"] = ll_procedures_df["Subcategory"].map(
        lambda x: None if pd.isnull(x) or x.strip() == "" else x.strip()
    )
    ll_procedures_df = ll_procedures_df[
        ll_procedures_df["Status"].map(
            lambda x: False if pd.isnull(x) else "approved" in x.lower().strip()
        )
    ]

    # Replace with All before ffill because of edge cases with merged cells
    ll_procedures_df.loc[
        ~pd.isnull(ll_procedures_df["ICF Topic"]) & pd.isnull(ll_procedures_df["TA"]),
        "TA",
    ] = "All"
    ll_procedures_df.loc[
        ~pd.isnull(ll_procedures_df["ICF Topic"])
        & pd.isnull(ll_procedures_df["Subcategory"]),
        "Subcategory",
    ] = "All"

    # Forward fill for edge cases
    ll_procedures_df["ICF Topic"] = ll_procedures_df["ICF Topic"].ffill()
    ll_procedures_df["TA"] = ll_procedures_df["TA"].ffill()
    ll_procedures_df["Subcategory"] = ll_procedures_df["Subcategory"].ffill()
    ll_procedures_df["ICF Section"] = ll_procedures_df["ICF Section"].map(
        lambda x: x.lower().strip()
    )
    ll_procedures_df["ICF Section"] = ll_procedures_df["ICF Section"].map(
        lambda x: ll_mapping[x] if x in ll_mapping else x
    )
    ll_procedures_df["Approved Adult Language"] = ll_procedures_df[
        "Approved Adult Language"
    ].map(lambda x: None if pd.isnull(x) or x.lower() == "not applicable" else x)
    ll_procedures_df = ll_procedures_df.dropna(subset="Approved Adult Language")

    return ll_procedures_df


def get_dct_df(path):
    dct_df = pd.read_excel(path, sheet_name="DCT ", dtype=str)
    dct_df = dct_df[
        dct_df["Status"].map(
            lambda x: False if pd.isnull(x) else "approved" in x.lower().strip()
        )
    ]

    dct_df["Vendor"] = dct_df["Vendor"].map(
        lambda x: (
            None if pd.isnull(x) or x.lower() == "any" or x.lower() == "N/A" else x
        )
    )

    dct_df["Vendor"] = dct_df["Vendor"].fillna("Other DCT")
    dct_df["ICF Topic"] = dct_df["ICF Topic"].map(
        lambda x: x.split("\n\n")[-1] if not pd.isnull(x) else ""
    )
    dct_df["UNIQUE_APPS"] = dct_df["Vendor"] + " - " + dct_df["ICF Topic"]
    dct_df = dct_df.set_index("UNIQUE_APPS")

    return dct_df



LL_PATH = "/dash/ICF-Language-Library_SSU_DSS_local.xlsx"

TA_DF = get_ta_df(LL_PATH)
STUDY_PROCEDURES_DF = get_ll_procedures_df(LL_PATH)
DCT_DF = get_dct_df(LL_PATH)


TAS = set(TA_DF["TA"]).union(set(STUDY_PROCEDURES_DF["TA"]))
TAS = sorted([ta for ta in TAS if "all" != ta.lower()])

SUBCATEGORIES = set(TA_DF["Subcategory"]).union(set(STUDY_PROCEDURES_DF["Subcategory"]))
SUBCATEGORIES = sorted([sub for sub in SUBCATEGORIES if "all" != sub.lower()])

