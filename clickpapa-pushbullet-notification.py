# Simple ClickPapa example,  to fetch unread messages from your dashboard
# and send them as a notification to your pushbullet account.
# Put this script into your crontab:
#
# */5 * * * * python /path/to/this/script/clickpapa-pushbullet-notification.py

import requests
import json

from pushbullet import Pushbullet
from HTMLParser import HTMLParser

# Get this token from https://clickpapa.com/profile
CLICKPAPA_ACCESS_TOKEN = ""

# Get this token from https://www.pushbullet.com/#settings
PUSHBULLET_ACCESS_TOKEN = ""

# How many notification will be sent per run
MAX_NOTIFICATION_PER_RUN = 3

# PushBullet
pb = Pushbullet(PUSHBULLET_ACCESS_TOKEN)

# ClickPapa messages have some HTML formatting, so we need to strip them out


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Token-based authentication can be considered a specialized version of
# Basic Authentication. The Authorization header tag will contain the auth
# token as the username, and no password.

# ClickPapa API support a "where" parameter, so we only going to fetch the
# messages where the read property is 0. We don't want to deal with
# pagination, so we just pass max_results=1000 to get all the items in the
# response.

sent = 0
for message in requests.get('https://api.clickpapa.io/v1/user/message?max_results=1000&where={"read":"0"}',
                            auth=(CLICKPAPA_ACCESS_TOKEN, '')).json()['_items']:

    # Check how many notification we sent in this session
    if sent < MAX_NOTIFICATION_PER_RUN:

        # Log to the console what messages going to be sent.
        print("#{} - {} : {} ".format(
            message['id'], message['title'], strip_tags(message['msg'])))

        # We send the notification via pushbullet
        push = pb.push_note(message['title'], strip_tags(message['msg']))
        sent += 1

    # Set the message to read, so we will not fetch it again. We do this for
    # every message regardless we sent a notification or not. So next time we
    # will only have unread messages.
    r = requests.patch("https://api.clickpapa.io/v1/user/message/{}".format(message['id']),
                       json.dumps({'read': 1}),
                       auth=(CLICKPAPA_ACCESS_TOKEN, ''),
                       headers={'Content-Type': 'application/json'}
                       )
