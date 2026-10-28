import json
import pydantic
from gliner2 import GLiNER2
from pathlib import Path

from fastapi import APIRouter, Depends

from app.models import Data

from .utils import *

from app.dependencies import get_model

router = APIRouter(tags=["data"])

DATA_FILE = Path(__file__).resolve().parents[3] / "data" / "mock.json"


@router.get("/data")
def get_data(model : GLiNER2 = Depends(get_model)) -> list[Data]:
    items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    dataList = [Data.model_validate(item) for item in items]

    for data in dataList:
        #replace references to sources in the content with actual links to them
        data.content = replace_sources_with_links(data)
        #anonymize any identifying details in the question
        data.question = anonymize_question(data.question, model)

    #find the icons for each link (if publicly accessible)
    add_icons_to_source_links(dataList)
    
    return dataList