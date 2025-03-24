from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
from app.models import TickerData, TickerDataCreate
from app import crud, strategy

app = FastAPI()

# Set up templates directory (make sure a folder named "templates" exists at the project root)
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Trading Strategy API"}

@app.get("/data", response_model=List[TickerData])
def get_all_data():
    data = crud.get_all_data()
    return data

@app.post("/data", response_model=TickerData)
def create_data(item: TickerDataCreate):
    new_item = crud.create_data(item)
    if new_item:
        return new_item
    raise HTTPException(status_code=400, detail="Error creating data")

@app.get("/strategy/performance")
def strategy_performance():
    """
    Returns the strategy performance as JSON.
    """
    performance = strategy.evaluate_strategy()
    return performance

@app.get("/strategy/performance/html", response_class=HTMLResponse)
def strategy_performance_html(request: Request):
    """
    Renders an HTML page showing the cumulative return, signal counts,
    and the complete dataset with signals.
    """
    performance = strategy.evaluate_strategy()
    return templates.TemplateResponse("strategy.html", {
        "request": request,
        "performance": performance
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
