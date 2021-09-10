import json
import time

import pandas as pd
import sqlalchemy as sa

import config

COMPANY_DOWNLOAD_URL = (
    "https://query1.finance.yahoo.com/v7/finance/download/{company}?period1={start}&period2={"
    "end}&interval={interval}&events=history&includeAdjustedClose=true "
)


def save_company__to_db(
    company: str,
    start_date: int = 0,
    end_date: int = int(time.time()),
    interval: str = "1d",
):
    df = pd.read_csv(
        COMPANY_DOWNLOAD_URL.format(
            company=company, start=start_date, end=end_date, interval=interval
        )
    )
    to_rename = df.columns.str.lower().str.split().str[0]
    df = df.rename(dict(zip(df.columns, to_rename)), axis=1)
    df.insert(loc=0, column="company", value=company)
    engine = sa.create_engine(config.DATABASE)
    df.to_sql("companies", con=engine, if_exists="append", index=False)


def fill_db():
    downloaded_companies = ["PD", "ZUO", "PINS", "ZM", "PVTL", "DOCU", "CLDR", "RUN"]
    for company in downloaded_companies:
        try:
            print(f"{company} is downloading")
            save_company__to_db(company)
        except Exception as e:
            print(repr(e))


def fetch_all_data(max_records: int):
    finances = _read_db()
    records = finances.head(max_records)
    return json.loads(records.to_json(orient="records"))


def fetch_data_for_company(company: str, max_records: int):
    finances = _read_db()
    if company not in finances["company"].unique():
        save_company__to_db(company)

    by_company = finances[finances["company"] == company].head(max_records)
    return json.loads(by_company.to_json(orient="records"))


def _read_db():
    engine = sa.create_engine(config.DATABASE)
    return pd.read_sql("companies", engine)