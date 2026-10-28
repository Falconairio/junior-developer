from app.models import *
from .constants import *
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
from gliner2 import GLiNER2
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
import favicon

#A function to take in the answer string and replace each <ref> with a link to the source
#Originally citing https://stackoverflow.com/questions/27006463/beautiful-soup-4-how-to-replace-a-tag-with-text-and-another-tag
#, that solution doesnt actually work as the string is not enclosed in html tags, so we cant insert after each ref, as there 
#is no parent to insert into. 
def replace_sources_with_links (dataObject : Data) -> str:
    soup = BeautifulSoup(dataObject.content,"html.parser")
    for ref in soup.find_all("ref"):
        newTag = soup.new_tag("a")
        populate_anchor_from_source(ref.text,newTag, dataObject.sources)
        ref.replace_with(newTag)
    #originally this read soup.get_text(), but the problem there is it stripped out the anchor tags, making it unsuitable for
    #displaying in the HTML. Simply stringifying the soup object preserves the anchors
    return str(soup)

#A simple function which will find the source from the source list via its id and populate the anchor element
def populate_anchor_from_source (id: str, tag: Tag, sources: list[Source]):
    for source in sources:
        if source.id == id:
            tag["href"] = source.source
            tag.string = source.title
    return ""

def find_favicon_from_source_link (sourceObject: Source) -> str:
    try:
        icons = favicon.get(sourceObject.source)
        for icon in icons:
            #grabbing the ico file specifically as its the most common form of icon that would be publicly accessible
            if(icon.format == "ico"):
                return icon.url
    #some sites do not allow gathering of icons in this way, so we must account for it
    except:
        print(f"Icon gathering forbidden for source {sourceObject.source}")
        return ""

#a method designed to reduce some of the computational burden of finding icons, as a lot of sources used in the examples
#are the same, and were wasting lots of time getting the same icons
def add_icons_to_source_links(dataList: list[Data]):
    searchedList = {}
    for data in dataList:
        for source in data.sources:
            #citation for https://bobbyhadz.com/blog/python-get-base-url
            url = urlparse(source.source)
            base = url.netloc
            #if this is a new source, get the favicon, otherwise use whats been saved already
            if(searchedList.get(base) == None):
                icon = find_favicon_from_source_link(source)
                source.icon = icon
                searchedList[base] = icon
            else:
                source.icon = searchedList.get(base)

#A function which extracts the likely identifying information and then anonymizes to the spec given for the exercise
def anonymize_question(question: str, model: GLiNER2) -> str:
    #get the keywords from the question
    #citation https://stackoverflow.com/questions/16819222/how-do-i-return-dictionary-keys-as-a-list-in-python
    extract = model.extract_entities(question, list(recognizerTypeDict.keys()), include_spans = True, include_confidence=True)

    #go through the entities and turn then into recognizer results
    recognizerResults = []
    for key in list(extract["entities"].keys()):
        for identitfication in extract["entities"][key]:
            recognizerResults.append(convert_extracted_entity_to_recognizer_result(identitfication,key))

    #anonymize using Presidio
    engine = AnonymizerEngine()
    result = engine.anonymize(
        text=question,
        analyzer_results=recognizerResults,
        operators=create_operator_map()
    )

    return result.text

#A function to convert the dictionaries returned from GLiNER2 to a recognizer result Presidio can use
def convert_extracted_entity_to_recognizer_result(entity, type) -> list[RecognizerResult]:
    return RecognizerResult(recognizerTypeDict[type],entity["start"],entity["end"], entity["confidence"])