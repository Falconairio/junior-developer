from presidio_anonymizer.entities import OperatorConfig

#using these dictionaries here as clean ways to not have to write out these conversions within our method logic
recognizerTypeDict = {
    "full_name": "PERSON",
    "first_name": "PERSON",
    "last_name": "PERSON",
    "email_address": "EMAIL_ADDRESS",
    "phone_number": "PHONE_NUMBER"
}

replacementTextDict = {
    "PERSON": "[NAME]",
    "EMAIL_ADDRESS": "[EMAIL]",
    "PHONE_NUMBER": "[PHONE]"
}

def create_operator_map():
    operators = {}
    for operator in list(replacementTextDict.keys()):
        operators[operator] = OperatorConfig("replace",{"new_value": replacementTextDict[operator]})
    return operators