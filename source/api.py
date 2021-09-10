from fastapi import FastAPI

from services import fetch_all_data, fetch_data_for_company

app = FastAPI()


@app.get("/companies/")
def get_all_finances(max_records: int = 100):
    records_json = fetch_all_data(max_records)
    return {"companies": records_json, "count": max_records}


@app.get("/companies/<company>")
def get_all_finances_by_company(company: str, max_records: int = 100):
    by_company_json = fetch_data_for_company(company, max_records)
    return {"companies": by_company_json, "count": max_records}