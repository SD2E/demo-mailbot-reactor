import json
import requests
from attrdict import AttrDict
from reactors.utils import Reactor, utcnow


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

    r.logger.info("Message: {}".format(m))
    r.logger.debug("Config: {}".format(r.settings))

    # Use JSONschema-based message validator
    # - In theory, this obviates some get() boilerplate
    if not r.validate_message(m):
        r.on_failure("Invalid message: {}".format(m))

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

    mailgunmessage = {'from': sender,
                      'to': recipient,
                      'subject': subject,
                      'text': body}

    if r.local is False:
        try:
            request = requests.post(
                mailgun_api_url,
                auth=('api', key),
                data=mailgunmessage)
        except Exception as e:
            r.on_failure("Error posting message: {}".format(e))

        r.on_success("Status: {} | Message: {}".format(
            request.status_code, request.text))
    else:
        r.logger.info("Skipped Mailgun API call since this is a test.")
        r.on_success("Status: {} | Message: {}".format(None, None))




if __name__ == '__main__':
    main()
