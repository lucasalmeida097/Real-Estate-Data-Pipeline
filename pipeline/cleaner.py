import pandas as pd
import json
from unidecode import unidecode


def normalize_text_columns(df: pd.DataFrame):
    text_columns = df.select_dtypes(include="object").columns
    for col in text_columns:
        df[col] = df[col].apply(lambda x: unidecode(x) if isinstance(x, str) else x)
    return df


def clean_properties(properties: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(properties)
    df = normalize_text_columns(df)

    df = df.drop_duplicates(subset=["title", "link"])

    df["details"] = df["details"].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )

    df["size"] = df["details"].apply(
        lambda x: int(float(x[0].replace("m²", "").replace(" ", "")))
        if isinstance(x, list) and len(x) > 0
        else None
    )
    df["bedrooms"] = df["details"].apply(
        lambda x: int(x[1].split(" ")[2])
        if isinstance(x, list) and len(x) > 1 and " a " in x[1]
        else int(x[1])
        if isinstance(x, list) and len(x) > 1 and x[1].isdigit()
        else None
    )
    df["parking_spaces"] = df["details"].apply(
        lambda x: int(x[2]) if isinstance(x, list) and len(x) > 2 else None
    )
    df["bathrooms"] = df["details"].apply(
        lambda x: int(x[3]) if isinstance(x, list) and len(x) > 3 else None
    )

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df.drop(columns=["details"], inplace=True)
    return df
