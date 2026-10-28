from pydantic import BaseModel


class Source(BaseModel):
    id: str
    title: str
    source: str
    #A personal addition, this is for holding the icon of the source site, if we can get it
    icon: str = ""


class Data(BaseModel):
    category: str
    question: str
    sources: list[Source]
    content: str
