import os
import json
from jsonschema import validate, FormatChecker, ValidationError

SCHEMA = '/message.jsonschema'
HERE = os.path.dirname(os.path.abspath(__file__))
MESSAGES = os.path.join(HERE, 'data', 'messages.json')


def validate_return_bool(object_json, schema_json, **kwargs):

        class formatChecker(FormatChecker):
            def __init__(self):
                FormatChecker.__init__(self)

        try:
            validate(object_json, schema_json, format_checker=formatChecker())
            return True
        except ValidationError:
            return False


def test_validate_message_schema():
    '''JSON schema validator works with message schema and JSON data'''

    with open(MESSAGES) as messages:
        messages_data = json.loads(messages.read())

    with open(SCHEMA) as schema_file:
        schema_json = json.loads(schema_file.read())

    for msg in messages_data:

        object_json = msg.get("object")
        expected_valid = msg.get("valid")

        is_valid = validate_return_bool(object_json, schema_json)

        if is_valid != expected_valid:
            raise(ValidationError(
                "Unexpected validation result for {}".format(object_json)))
