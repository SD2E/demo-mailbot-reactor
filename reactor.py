import json
import requests
from attrdict import AttrDict
from jsonschema import validate, RefResolver
from reactors.utils import Reactor, utcnow


def validate_json_message(messageJSON='{}',
                          messageschema='/message.jsonschema',
                          permissive=True):
    """
    Validate JSON string against a JSON schema

    Positional arguments:
    messageJSON - str - JSON text

    Keyword arguments:
    schema_file - str - path to the requisite JSON schema file
    permissive - bool - swallow validation errors [False]
    """
    try:
        with open(messageschema) as schema:
            schema_json = json.loads(schema.read())
            schema_abs = 'file://' + messageschema
    except Exception as e:
        if permissive is False:
            raise Exception("schema loading error", e)
        else:
            return False

    class fixResolver(RefResolver):
        def __init__(self):
            RefResolver.__init__(self, base_uri=schema_abs, referrer=None)
            self.store[schema_abs] = schema_json

    try:
        validate(messageJSON, schema_json, resolver=fixResolver())
        return True
    except Exception as e:
        if permissive is False:
            raise Exception("message validation failed", e)
        else:
            return False


def main():
    """
    Main function for sending a message.

    Input message(s):
        {"to": "travolta@swordfi.sh", "subject":
            "How do I find this guy?", "body": "You don't find him;
                he finds you"}

    Output message(s):
        N/A

    Linked actors:
        N/A
    """
    r = Reactor()
    m = AttrDict(r.context.message_dict)

    r.logger.debug("Config: {}".format(r.settings))
    r.logger.debug("Message: {}".format(m))

    key = r.settings.get('api_key', None)
    if key is None:
        r.on_failure("No Mailgun API key was provided.")

    mailgun_api_url = r.settings.get('mailgun_api_url', None)
    if mailgun_api_url is None:
        r.on_failure("No Mailgun API URL was specified.")

    sender = r.settings.get('from', 'reactors-noreply@sd2e.org')
    recipient = m.get('to', None)
    if recipient is None:
        r.on_failure("No recipient was specified. What are you doing?")

    try:
        # Message subject line
        subject = m.get('subject', r.settings.get(
            'subject', 'Automated email notification'))
        # Message body
        ts = utcnow()
        body = "Message sent at {} by actors/{}/executions/{}".format(
            ts, r.uid, r.execid)
        body = m.get('body', body)
    except Exception as e:
        r.on_failure("Error setting up message: {}".format(e))

    try:
        request = requests.post(
            mailgun_api_url,
            auth=('api', key),
            data={'from': sender,
                  'to': recipient,
                  'subject': subject,
                  'text': body})
    except Exception as e:
        r.on_failure("Error posting message: {}".format(e))

    r.on_success("Status: {} | Message: {}".format(
        request.status_code, request.text))


if __name__ == '__main__':
    main()
