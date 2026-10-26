from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/api/overview/year")
def by_year():
    df = pd.read_csv("prepared_data/clean_data.csv")
    order = ["Freshman", "Sophomore", "Junior", "Senior"]
    g = df.groupby("University_Year")["placement_status_binary"].mean().reindex(order)
    return {"labels": order, "values": g.values.tolist()}